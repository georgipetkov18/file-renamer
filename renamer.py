import os

CONTAINER_TEMPLATE = '<c>'
clear_console = lambda: os.system('cls')

def print_main_menu():
    print('0.Exit')
    print('1.Basic Rename - rename files using your input and incrementing a counter afterwards')
    print('2.Continuous Rename - rename files in a folder using the naming pattern of another folder')


def execute_basic_rename(path):
    counter = 0
    path = path if path else os.getcwd()

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_full = os.path.join(dirpath, filename)
            if file_full == os.path.abspath( __file__ ):
                continue
            
            name, extension = os.path.splitext(file_full)
            new_name = f'{new_name_input} ({counter}){extension}'
            new_file_full = os.path.join(dirpath, new_name)
            
            os.rename(file_full, new_file_full)
            counter += 1


print_main_menu()
while True:
    input_option = int(input())

    if input_option == 0:
        print('Exiting...')
        break

    elif input_option == 1:
        clear_console()

        print('Enter new name for the files')
        new_name_input = input()

        print('-' * 50)

        print('Enter the path to the folder where the files are located')
        path = input()
        execute_basic_rename(path)

        clear_console()
        print('Done')
        break

    elif input_option == 2:
        pass

    else:
        clear_console();
        print('Invalid option. Choose again')
        print_main_menu()
