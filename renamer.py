import os
import re

CONTAINER_TEMPLATE = '<c>'
clear_console = lambda: os.system('cls')

def print_main_menu():
    print('0.Exit')
    print('1.Basic Rename - rename files using your input and incrementing a counter afterwards')
    print('2.Pattern Based Rename - rename files based on an input pattern')


def get_details_info():
    print('Enter the path to the folder where the files are located')
    path = input()
    counter = 0

    while True:
        print('Do you want to enter an initial number y/n')
        init_num = input()

        if init_num.lower() == 'y':
            print('Enter initial number')
            counter = int(input())
            break

        elif init_num.lower() == 'n':
            break

        else:
            continue

    clear_console()
    return (path, counter)


def execute_basic_rename(path, name_input, counter = 0):
    path = path if path else os.getcwd()

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_full = os.path.join(dirpath, filename)
            if file_full == os.path.abspath( __file__ ):
                continue
            
            _, extension = os.path.splitext(file_full)
            new_name = f'{name_input} ({counter}){extension}'
            new_file_full = os.path.join(dirpath, new_name)
            
            os.rename(file_full, new_file_full)
            counter += 1


def execute_pattern_based_rename(path, input_pattern, container_template, counter = 0, digits_count = None):
    path = path if path else os.getcwd()

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_full = os.path.join(dirpath, filename)
            if file_full == os.path.abspath( __file__ ):
                continue
            
            _, extension = os.path.splitext(file_full)
            counter_str = str(counter)
            counter_digits_count = len(str(counter))
            counter_cont = counter_str if digits_count == None else f'{"0" * (digits_count - counter_digits_count)}{counter_str}'
            new_name = f'{input_pattern.replace(container_template, counter_cont)}{extension}'
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

        path, counter = get_details_info()
        execute_basic_rename(path, new_name_input, counter)

        print('Done')
        break

    elif input_option == 2:
        digits_count = None
        clear_console()

        while True:
            print(f'Enter your pattern, replacing the variable part of the sequence with {CONTAINER_TEMPLATE}')
            print(f'e.g. example - {CONTAINER_TEMPLATE} ---> example - 1 ---> example - 2, etc.')
            input_pattern = input()
            res = re.search('<c(:d\d+)?>', input_pattern)
            match = CONTAINER_TEMPLATE

            if res:
                span = res.span()
                match = input_pattern[span[0]:span[1]]
                match_split = match.strip('<>').split(':d')
                if len(match_split) > 1:
                    digits_count = int(match_split[1])
                break

            clear_console()
            print('Invalid Pattern') 

        print('-' * 50)

        path, counter = get_details_info()
        execute_pattern_based_rename(path, input_pattern, match, counter, digits_count)

        print('Done')
        break

    else:
        clear_console();
        print('Invalid option. Choose again')
        print_main_menu()

