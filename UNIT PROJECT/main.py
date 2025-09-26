from functions import *
import sqlite3
# MAIN FUNCTION
# - JT
def main():
    title = f'''{colors['BLUE']}
----------------------------------------------------------------------------------------------
  ____                _____   ______                        _____              __  __   _____    
 |  _ \      /\      / ____| |  ____|                      / ____|     /\     |  \/  | |  __ \   
 | |_) |    /  \    | (___   | |__                        | |         /  \    | \  / | | |__) |  
 |  _ <    / /\ \    \___ \  |  __|                       | |        / /\ \   | |\/| | |  ___/   
 | |_) |  / ____ \   ____) | | |____                      | |____   / ____ \  | |  | | | |       
 |____/  /_/    \_\ |_____/  |______|                      \_____| /_/    \_\ |_|  |_| |_|       
  _____    ______    _____   _____   _____    ______       ____     ____     ____    _  __       
 |  __ \  |  ____|  / ____| |_   _| |  __ \  |  ____|     |  _ \   / __ \   / __ \  | |/ /       
 | |__) | | |__    | |        | |   | |__) | | |__        | |_) | | |  | | | |  | | | ' /        
 |  _  /  |  __|   | |        | |   |  ___/  |  __|       |  _ <  | |  | | | |  | | |  <         
 | | \ \  | |____  | |____   _| |_  | |      | |____      | |_) | | |__| | | |__| | | . \        
 |_|  \_\ |______|  \_____| |_____| |_|      |______|     |____/   \____/   \____/  |_|\_\   

----------------------------------------------------------------------------------------------                                                                                                   
'''                                                                                                 
    connection = sqlite3.connect('recipes.db')
    cursor = connection.cursor()
    create_database(connection, cursor)
    while True:
        clear()
        print(title)
        print(f'{colors['RESET']}What would you like to do?')
        print(f'{colors['CYAN']}[View] Recipes')
        print(f'{colors['GREEN']}[Add] Recipe')
        print(f'{colors['RED']}[Delete] Recipe')
        print(f'{colors['MAGENTA']}[Export] Recipe')
        print(f'{colors['YELLOW']}[Modify] Recipe')
        print(f'{colors['RESET']}[Quit]')
        print()
        option = input('> ')
        match option.lower():
            case 'view':
                clear()
                view(connection, cursor)
            case 'add':
                clear()
                add(connection, cursor)
            case 'delete':
                clear()
                delete(connection, cursor)
            case 'export':
                clear()
                export(connection, cursor, None)
            case 'modify':
                clear()
                modify(connection, cursor, None)
            case 'quit':
                connection.close()
                quit()
            case _:
                input('Invalid Option. ENTER to return to title.')
        
if __name__ == '__main__':
    main()