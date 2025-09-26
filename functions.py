import os
from fpdf import FPDF
from tabulate import tabulate
# COLORS FOR TERMINAL TEXT
colors = {
    'BLACK':'\033[30m',
    'RED' : '\033[31m',
    'GREEN' :'\033[32m',
    'YELLOW' : '\033[33m',
    'BLUE' : '\033[34m',
    'MAGENTA' : '\033[35m',
    'CYAN' : '\033[36m',
    'WHITE' : '\033[37m',
    'RESET' : '\033[0m'
    }

# PDF TEMPLATE
class RecipePDF(FPDF):
    def header(self):
        # Optional: Add a header with the recipe title
        self.set_font("Arial", "B", 24)
        self.cell(0, 10, self.title, 0, 1, "C") # type: ignore
        self.ln(10)

    def footer(self):
        # Optional: Add a footer with page numbers or other info
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        # Add a section title for ingredients or instructions
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def chapter_body(self, body):
        # Add the main content of the section, with automatic line breaks
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln(5)

# CLEAR FUNCTION
def clear():
        # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
        # For macOS and Linux
    else:
        _ = os.system('clear')
        
# CHECK NAME
def check_name(cursor, name_input):
    cursor.execute('SELECT name FROM Recipes')
    names = cursor.fetchall()
    valid = False
    for name in names:
        if name_input in name:
            valid = True
            break
        else:
            valid = False
    return valid

# CREATE DATABASE FUNCTION
def create_database(connection, cursor):
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Recipes ( 
                name TEXT NOT NULL,
                difficulty INTEGER ,
                rating FLOAT,
                category TEXT NOT NULL,
                cook_time INTEGER ,
                serving_size INTEGER ,
                ingredients TEXT NOT NULL,
                directions TEXT NOT NULL
                )
                ''')
    
# PRINT TABLE FUNCTION
def print_table(cursor):
    # Used in the view function to print the table in the terminal.
    data = cursor.fetchall()
    headers = ('Name', 'Difficulty (1-5)','Rating (1-5)', 'Category', 'Cook Time (min.)', 'Serving Size', 'Ingredients')
    print(tabulate(data, headers=headers, tablefmt="grid"))

# VIEW FUNCTION
def view(connection, cursor):
    # Options for the user to sort by
    options = ('name', 'difficulty','rating', 'category', 'cook_time', 'serving_size')
    # Loop prints out each option in the correct format
    print(f'{colors['CYAN']}What item would you like to view?')
    for option in options:
        print(f'[{option.upper().replace('_',' ')}]')
    print('[RETURN] to title.')
    print(f'{colors['RESET']}')
    user_input = input('> ').lower()
    base_query = "SELECT name, difficulty, rating, category, cook_time, serving_size FROM Recipes"
    # Orders the table by the user's desiered input
    if user_input == 'return':
        return
    else:
        for option in options:
            if user_input.replace(' ', '_') == option:
                cursor.execute(f'{base_query} ORDER BY {user_input.replace(' ','_')}')
                print_table(cursor)
    # SELECTING A RECIPE FROM TABLE
    print()
    print('Which recipe would you like to open?')
    print('[RETURN] to title')
    name_input = input('> ')
    if name_input.lower() == 'return':
        return
    valid = check_name(cursor, name_input)
    if valid:
        # When the user selects a recipe from the table, this opens th recipe with more details and prompts the user to export or modify
        clear()
        cursor.execute(f"SELECT * FROM Recipes WHERE name = '{name_input}'")
        recipe = cursor.fetchall()
        name = recipe[0][0]
        difficulty = str(recipe[0][1])
        rating = str(recipe[0][2])
        category = recipe[0][3]
        cook_time = str(recipe[0][4])
        serving_size = str(recipe[0][5])
        ingredients = recipe[0][6].split(', ')
        directions = recipe[0][7].split(', ')
        print(f'{colors['RESET']}{name}')
        print(f'{colors['BLUE']}Category: {category}')
        print(f'{colors['RED']}Difficulty: {difficulty}/5')
        print(f'{colors['YELLOW']}Rating: {rating}/5')
        print(f'{colors['GREEN']}Cook Time: {cook_time} min.')
        print(f'{colors['MAGENTA']}Serving Size: {serving_size} people')
        print()
        print(f'{colors['CYAN']}Ingredients:')
        for ingredient in ingredients:
            print(f'- {ingredient}')
        print()
        print(f'{colors['BLUE']}Directions:')
        for step in directions:
            print(step)
        print(f'''{colors["RESET"]}
[RETURN] to title
[EXPORT] Recipe
[MODIFY] Recipe
              ''')
        option = input('> ')
    # Allow User to Export or Modify from full screen recipe. (refer to video)
        match option.lower():
            case 'return':
                pass
            case 'export':
                clear()
                export(connection, cursor, name)
            case 'modify':
                clear()
                modify(connection, cursor, name)
            case _:
                clear()
                print('Invalid Option.')
                input('Press ENTER to return to Title.')
    
# ADD FUNCTION
def add(connection, cursor):
    # Askes the user for all the info for a recipe
    print(f'{colors['GREEN']}')
    print('[RETURN] to title.')
    print("What is the name of the recipe you would like to add?")
    name = input("> ")
    if name.lower() == 'return':
        return
    print("What is the diffuclty of the recipe you would like to add?(0-5)")
    difficulty = input("> ")
    if difficulty.lower() == 'return':
        return
    print("What is the rating of the recipe you would like to add? (0.0-5.0)")
    rating = input("> ")
    if rating.lower() == 'return':
        return
    print("What is the category of the recipe you would like to add?")
    category = input("> ")
    if category.lower() == 'return':
        return
    print("What is the cook time of the recipe you would like to add? (min.)")
    cook_time = input("> ")
    if cook_time.lower() == 'return':
        return
    print("What is the serving size of the recipe you would like to add?")
    serving_size = input("> ")
    if serving_size.lower() == 'return':
        return
    print("What is the ingredients of the recipe you would like to add?")
    print('Seperate ingredients with commas. Example:')
    print('Apple, Orange, Pear, Bananna')
    ingredients = input("> ")
    if ingredients.lower() == 'return':
        return
    print("What is the directions of the recipe you would like to add?")
    print('Seperate ingredients with commas. Example:')
    print('Step 1: Get Bowl, Step 2: Pour Cereal, Step 3: Pour Milk')
    directions = input("> ")
    if directions.lower() == 'return':
        return
    cursor.execute(f'INSERT INTO Recipes VALUES("{name}", "{difficulty}","{rating}","{category}", "{cook_time}", "{serving_size}", "{ingredients}", "{directions}")')
    connection.commit()
    clear()
    print('Recipe Added.')
    input('Press ENTER to return to Title.')


# DELETE FUNCTION
def delete(connection, cursor):
    # User selects a recipe and deletes it from the database
    print(f'{colors['RED']}')
    print('[RETURN] to title')
    print("What is the name of the recipe you would like to delete?")
    name_input = input('> ')
    if name_input.lower() == 'return':
        return
    valid = check_name(cursor, name_input)
    if valid:
        cursor.execute (f'DELETE FROM Recipes WHERE name = "{name_input}"')
        connection.commit()
        print(f"{name_input} has been deleted from your recipes.")
    else:
        print('Recipe Not Found')
    input('Press ENTER to return to Title.')

# EXPORT FUNCTION
def export(connection, cursor, name):
    print(f'{colors['MAGENTA']}')
    if name == None:
        print('[RETURN] to title')
        print('What is the name of the recipe?')
        name_input = input('> ')
        if name_input.lower() == 'return':
            return
    else:
        name_input = name
    valid = check_name(cursor, name_input)
    if valid:
        # Fetch recipe data
        cursor.execute(f"SELECT * FROM Recipes WHERE name = '{name_input}'")
        recipe = cursor.fetchall()
        name = recipe[0][0]
        difficulty = str(recipe[0][1])
        rating = str(recipe[0][2])
        category = recipe[0][3]
        cook_time = str(recipe[0][4])
        serving_size = str(recipe[0][5])
        ingredients = recipe[0][6].replace(', ', '\n')
        directions = recipe[0][7].replace(', ', '\n')
        filename = f'{name.lower()}_recipe.pdf'
        # CREATE PDF
        pdf = RecipePDF()
        pdf.set_title(name)
        pdf.add_page()
        pdf.set_margins(20, 20, 20)
        
        # CATEGORY
        pdf.chapter_title(f'Category: {category}')
        # DIFFICULTY
        pdf.chapter_title(f'Difficulty: {difficulty}/5')
        # RATING
        pdf.chapter_title(f'Rating: {rating}/5.0')
        # COOK TIME
        pdf.chapter_title(f'Cook Time: {cook_time} min.')
        # SERVING SIZE
        pdf.chapter_title(f'Serves {serving_size} people.')
        # INGREDIENTS
        pdf.chapter_title('Ingredients:')
        pdf.chapter_body(ingredients)
        # DIRECTIONS
        pdf.chapter_title('Directions:')
        pdf.chapter_body(directions)
        # OUTPUT
        pdf.output(filename)
        print(f'{filename} created successfully!')
    else:
        print('Recipe Not Found.')
    input('Press ENTER to return to Title.')

# MODIFY FUNCTION
def modify(connection, cursor, name):
    print(f'{colors['YELLOW']}')
    print('[RETURN] to title.')
    if name == None:
        print("Which recipe would you like to update?")
        name_input = input('> ')
        if name_input.lower() == 'return':
            return
    else:
        name_input = name
    valid = check_name(cursor, name_input)
    if valid:
        # Allows the user to select a category and update it
        print("What would you like to update?")
        i = input("> ")
        if i.lower() == 'return':
            return
        if i.lower() == "name":
            print("What would you like to change the name to?")
            n = input("> ")
            cursor.execute(f'update Recipes set name = "{n}" where name = "{name_input}"')
        elif i.lower() == "difficulty":
            print("What would you like to change the difficulty to?")
            d = input("> ")
            cursor.execute(f'update Recipes set difficulty = "{d}" where name = "{name_input}"')
        elif i.lower() == "category":
            print("What would you like to change the category to?")
            c = input("> ")
            cursor.execute(f'update Recipes set category = "{c}" where name = "{name_input}"')
        elif i.lower() == "cook time":
            print("What would you like to change the cook time to?")
            co = input("> ")
            cursor.execute(f'update Recipes set cook_time = "{co}" where name = "{name_input}"')
        elif i.lower() == "serving size":
            print("What would you like to change the serving size to?")
            s = input("> ")
            cursor.execute(f'update Recipes set serving_size = "{s}" where name = "{name_input}"')
        elif i.lower() == "ingredients":
            print("What would you like to change the ingredients to?")
            i = input("> ")
            cursor.execute(f'update Recipes set ingredients = "{i}" where name = "{name_input}"')
        elif i.lower() == "directions":
            print("What would you like to change the directions to?")
            d = input("> ")
            cursor.execute(f'update Recipes set directions = "{d}" where name = "{name_input}"')
        elif i.lower() == "rating":
            print("What would you like to change the raiting to?")
            r = input("> ")
            cursor.execute(f'update Recipes set directions = "{r}" where name = "{name_input}"')
        else:
            print("That is not a category. Please select from Name, Difficulty, Category, Cook Time, Serving Size, Ingredients, Rating, or Directions.")
        connection.commit()
        print('Modification Successful.')
    else:
        print("Invalid Name")
    input('Press ENTER to return to Title.')