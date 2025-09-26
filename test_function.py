import sqlite3
import pytest
from functions import *
def test_add_recipe(monkeypatch, capsys):
    # Prepare a list of mock inputs for every input() call
    mock_inputs = iter([
        'Fruit Salad', '2', '4.5', 'Dessert', '10', '2',
        'Apple, Banana, Orange', 
        'Step 1: Chop fruit, Step 2: Mix together',
        ''  # final input for "Press ENTER to return to Title"
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(mock_inputs))

    # Setup in-memory database
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Recipes (
        name TEXT, difficulty INTEGER, rating FLOAT, category TEXT,
        cook_time INTEGER, serving_size INTEGER,
        ingredients TEXT, directions TEXT
    )''')

    # Run function
    add(conn, cur)

    # Validate insertion
    cur.execute("SELECT * FROM Recipes WHERE name='Fruit Salad'")
    result = cur.fetchone()
    assert result is not None
    assert result[0] == 'Fruit Salad'
    assert result[1] == 2
    assert result[2] == 4.5

    # Validate output
    captured = capsys.readouterr()
    assert "Recipe Added." in captured.out

def test_delete_existing_recipe(monkeypatch, capsys):
    # Simulated user inputs: 'Pancakes' and then ENTER
    monkeypatch.setattr('builtins.input', lambda _: next(inputs := iter(['Pancakes', ''])))

    # Patch check_name to return True
    monkeypatch.setattr(__name__ + '.check_name', lambda cur, name: True)

    # Setup in-memory DB
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Recipes (
        name TEXT, difficulty INTEGER, rating FLOAT, category TEXT,
        cook_time INTEGER, serving_size INTEGER,
        ingredients TEXT, directions TEXT
    )''')
    # Add a recipe to delete
    cur.execute('''INSERT INTO Recipes VALUES (
        "Pancakes", 2, 4.5, "Breakfast", 10, 2, "Flour, Eggs, Milk", "Mix and fry"
    )''')
    conn.commit()

    # Run delete function
    delete(conn, cur)

    # Validate recipe was deleted
    cur.execute("SELECT * FROM Recipes WHERE name='Pancakes'")
    assert cur.fetchone() is None

    # Validate output
    captured = capsys.readouterr()
    assert "Pancakes has been deleted from your recipes." in captured.out

def test_delete_recipe_not_found(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: next(inputs := iter(['FakeRecipe', ''])))
    monkeypatch.setattr(__name__ + '.check_name', lambda cur, name: False)

    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Recipes (
        name TEXT, difficulty INTEGER, rating FLOAT, category TEXT,
        cook_time INTEGER, serving_size INTEGER,
        ingredients TEXT, directions TEXT
    )''')

    delete(conn, cur)

    captured = capsys.readouterr()
    assert "Recipe Not Found" in captured.out

def test_delete_return_early(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'return')

    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Recipes (
        name TEXT, difficulty INTEGER, rating FLOAT, category TEXT,
        cook_time INTEGER, serving_size INTEGER,
        ingredients TEXT, directions TEXT
    )''')

    delete(conn, cur)

    captured = capsys.readouterr()
    assert "What is the name of the recipe you would like to delete?" in captured.out
    assert "has been deleted" not in captured.out
    assert "Recipe Not Found" not in captured.out

def test_export_return_input(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'return')

    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()

    export(conn, cur, None)

    captured = capsys.readouterr()
    assert "What is the name of the recipe?" in captured.out
    assert "Exporting" not in captured.out
    assert "Recipe not found." not in captured.out


def test_view_function(monkeypatch, capsys):
    # Set up test DB
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    create_database(conn, cur)

    # Insert a sample recipe
    cur.execute('''INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
        "Sample Recipe", 3, 4.5, "Dessert", 20, 2, "Sugar, Flour", "Mix, Bake"
    ))
    conn.commit()

    # Simulate user input for:
    # 1. Sorting by 'rating'
    # 2. Selecting 'Sample Recipe'
    # 3. Choosing 'return' at the end
    inputs = iter(["rating", "Sample Recipe", "return"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Call the view function
    view(conn, cur)

    # Check the output
    captured = capsys.readouterr()
    assert "Sample Recipe" in captured.out
    assert "Difficulty: 3/5" in captured.out
    assert "Rating: 4.5/5" in captured.out
    assert "Category: Dessert" in captured.out
    assert "Cook Time: 20 min." in captured.out
    assert "Serving Size: 2 people" in captured.out






  