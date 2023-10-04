import tkinter as tk
import ast

LARGE_FONT_STYLE = ("Arial", 36, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)
        }
        self.operations = {'/': '÷', '*': '×', '-': '-', '+': '+'}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_clear_entry_button()
        self.bind_keys()

    def bind_keys(self):
        # Bind Return key to evaluate expression
        self.window.bind("<Return>", lambda event: self.evaluate())
        # Bind number and operator keys to corresponding functions
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

        # Bind '=' key to evaluate expression
        self.window.bind("=", lambda event: self.evaluate())

        # Bind backspace key to delete the last character
        self.window.bind("<BackSpace>", lambda event: self.delete_last_character())

    def delete_last_character(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.update_label()

    def create_special_buttons(self):
        # Create buttons for equals, square, and square root
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        # Create label to display total expression
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        # Create label to display current expression
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        # Create frame for displaying expressions
        frame = tk.Frame(self.window, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        # Function to add digits and decimal point to current expression
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        # Create buttons for digits and decimal point
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg="white", fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        # Function to append operators to the current expression
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        # Create buttons for arithmetic operators
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg="#F0F0F0", fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=3, sticky=tk.NSEW)
            i += 1

    def clear(self):
        # Function to clear the expressions
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        self.label.config(font=LARGE_FONT_STYLE)

    def create_clear_entry_button(self):
        # Create "CE" button to clear the current expression
        button = tk.Button(self.buttons_frame, text="CE", bg="#F0F0F0", fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=0, sticky=tk.NSEW)

    def square(self):
        # Function to calculate square of the current expression
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        # Create "x²" button to calculate square
        button = tk.Button(self.buttons_frame, text="x²", bg="#F0F0F0", fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def sqrt(self):
        # Function to calculate square root of the current expression
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        # Create "√" button to calculate square root
        button = tk.Button(self.buttons_frame, text="√", bg="#F0F0F0", fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def evaluate(self):
        # Function to evaluate the expression and display result
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            node = ast.parse(self.total_expression, mode='eval')
            result = eval(compile(node, '<string>', 'eval'))
            self.current_expression = str(result)
            self.total_expression = ""
        except ZeroDivisionError:
            self.current_expression = "Division by zero"
        except SyntaxError:
            self.current_expression = "Invalid expression"
        except Exception as e:
            self.current_expression = "Error"

        self.update_label()

    def create_equals_button(self):
        # Create "=" button to evaluate the expression
        button = tk.Button(self.buttons_frame, text="=", bg="#FF9500", fg="white", font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=2, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        # Create frame for calculator buttons
        frame = tk.Frame(self.window, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        # Update the label with the total expression
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        # Limit the length of the current expression to fit the label
        # self.label.config(text=self.current_expression[:15])
        self.label.config(text=self.current_expression)
        if len(self.current_expression) > 15:
            self.label.config(font=("Arial", int(30 - len(self.current_expression) / 2)))
            self.label.config(text=self.current_expression)

    def run(self):
        # Start the GUI event loop
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
