import os, re
import tkinter as tk
from tkinter import ttk, filedialog

class Renamer:
    def execute_basic_rename(filenames, name_input, counter = 0):
        for filename in filenames:
            if filename == os.path.abspath( __file__ ):
                continue
            dirname = os.path.dirname(filename)
            _, extension = os.path.splitext(filename)
            
            new_name = f'{name_input} ({counter}){extension}'
            new_filename = os.path.join(dirname, new_name)
            
            os.rename(filename, new_filename)
            counter += 1

    def execute_pattern_based_rename(filenames, input_pattern, container_template, counter = 0, digits_count = None):
        for filename in filenames:
            if filename == os.path.abspath( __file__ ):
                continue

            dirname = os.path.dirname(filename)
            _, extension = os.path.splitext(filename)
            counter_str = str(counter)
            counter_digits_count = len(str(counter))
            counter_cont = counter_str if digits_count == None else f'{"0" * (digits_count - counter_digits_count)}{counter_str}'
            new_name = f'{input_pattern.replace(container_template, counter_cont)}{extension}'
            new_filename = os.path.join(dirname, new_name)
            
            os.rename(filename, new_filename)
            counter += 1


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('File Renamer')
        self.geometry('450x300')
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.radio_var = tk.IntVar()

        vcmd_num = (self.register(self.validate_number), '%P')
        ivcmd_num = (self.register(self.on_invalid_number),)

        vcmd_pattern = (self.register(self.validate_pattern), '%P')
        ivcmd_pattern = (self.register(self.on_invalid_pattern),)


        # initial number block
        ttk.Label(self, text='Initial Number:').grid(row=0, column=0, pady=10)
        self.init_number_field = ttk.Entry(self, width=10)
        self.init_number_field.config(validate='focusout', validatecommand=vcmd_num, invalidcommand=ivcmd_num)
        self.init_number_field.grid(row=0, column=1, sticky=tk.S, pady=10)

        self.label_error_number = ttk.Label(self, foreground='red')
        self.label_error_number.grid(row=1, column=1, sticky=tk.NS, padx=5)

        # name or pattern block
        ttk.Label(self, text='Name or pattern:').grid(row=2, column=0, pady=10)
        self.pattern_field = ttk.Entry(self, width=30)
        self.pattern_field.config(validate='focusout', validatecommand=vcmd_pattern, invalidcommand=ivcmd_pattern)
        self.pattern_field.grid(row=2, column=1)

        self.label_error_pattern = ttk.Label(self, foreground='red')
        self.label_error_pattern.grid(row=3, column=1, sticky=tk.NS, padx=5)
        
        # radio buttons block
        self.basic_rename_btn = ttk.Radiobutton(self, text='Basic Rename', variable=self.radio_var, value=0)
        self.basic_rename_btn.grid(row=4, column=0)

        self.pattern_based_rename_btn = ttk.Radiobutton(self, text='Pattern Based Rename', variable=self.radio_var, value=1)
        self.pattern_based_rename_btn.grid(row=4, column=1)


        # button
        self.send_button = ttk.Button(text='Choose Files', command=self.select_files).grid(row=5, column=0, columnspan=2, pady=10)

    def show_message_number(self, error='', color='black'):
        self.label_error_number['text'] = error
        self.init_number_field['foreground'] = color

    def show_message_pattern(self, error='', color='black'):
        self.label_error_pattern['text'] = error
        self.pattern_field['foreground'] = color

    def validate_number(self, value):
        if str.isdigit(value) or value == '':
            self.show_message_number('', 'black')
            return True

        return False

    def validate_pattern(self, value):
        if value and self.radio_var.get() == 0:
            self.show_message_pattern('', 'black')
            return True

        res = re.search('<c(:d\d+)?>', value)
        if res:
            self.pattern_info = res
            self.show_message_pattern('', 'black')
            return True

        return False

    def on_invalid_number(self):
        self.show_message_number('Please enter a number', 'red')

    def on_invalid_pattern(self):
        self.show_message_pattern('Please enter a valid pattern', 'red')

    def select_files(self):
        num_val = self.init_number_field.get()
        pat_val = self.pattern_field.get()
        if not self.validate_number(num_val):
            self.on_invalid_number()
            return

        if not self.validate_pattern(pat_val):
            self.on_invalid_pattern()
            return

        filetypes = (
            ('All files', '*.*'),
        )

        filenames = filedialog.askopenfilenames(
            title='Choose files',
            initialdir='/',
            filetypes=filetypes)

        radio_value = self.radio_var.get()
        counter = int(self.init_number_field.get()) if self.init_number_field.get() else 0
        if radio_value == 0:
            Renamer.execute_basic_rename(filenames, self.pattern_field.get(), counter)

        elif radio_value == 1:
            digits_count = None
            input_pattern = self.pattern_field.get()
            span = self.pattern_info.span()
            match = input_pattern[span[0]:span[1]]
            match_split = match.strip('<>').split(':d')

            if len(match_split) > 1:
                digits_count = int(match_split[1])

            Renamer.execute_pattern_based_rename(filenames, input_pattern, match, counter, digits_count)

app = App()
app.mainloop()