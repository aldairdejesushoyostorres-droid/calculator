import tkinter as tk
from tkinter import messagebox
import calculator
import history_manager

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Python Calculator")

        # --- History Management ---
        self.history = history_manager.load_history()

        # --- State Variables ---
        self.current_input = ""
        self.last_result = None
        self.pending_operation = None # Stores the option code for basic_operations
        self.first_operand = None

        # --- UI Setup ---
        
        # 1. Display
        self.display = tk.Entry(master, width=30, borderwidth=5, font=('Arial', 16), justify='right')
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # 2. Buttons (Numbers and Basic Ops)
        self.create_buttons()

        # 3. History Button
        self.history_btn = self.create_btn("History", lambda: self.show_history(), 1, 4, color='orange')
        
        # 4. Advanced Functions Button
        self.adv_btn = self.create_btn("Functions", lambda: self.show_advanced_menu(), 2, 4, color='lightblue')
        
        # Configure closing protocol to save history
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_btn(self, text, command, row, col, columnspan=1, color='lightgray'):
        """Helper function to create and place a button."""
        button = tk.Button(self.master, text=text, padx=20, pady=20, command=command, bg=color, font=('Arial', 12))
        button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew")
        return button

    def create_buttons(self):
        """Creates number, operator, and special buttons."""
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3, 2),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3, 1),
            ('=', 5, 3, 2)
        ]
        
        # Basic Operation map for calculator.basic_operations()
        self.op_map = {'+': 1, '-': 2, '*': 3, '/': 4, '%': 5, '^': 6}

        r = 0
        for (text, row, col, *op_key) in buttons:
            if text.isdigit() or text == '.':
                self.create_btn(text, lambda t=text: self.number_click(t), row, col)
            elif text in self.op_map:
                op_code = self.op_map[text]
                self.create_btn(text, lambda op=op_code: self.operator_click(op), row, col, color='#FFC107')
            elif text == 'C':
                self.create_btn(text, self.clear_display, row, col, color='red')
            elif text == '=':
                self.create_btn(text, self.calculate, row, col, columnspan=op_key[0], color='green')
                r=row
        
        # Adding Modulo and Power to the basic layout
        self.create_btn('%', lambda: self.operator_click(self.op_map['%']), r+1, 0, color='#FFC107')
        self.create_btn('^', lambda: self.operator_click(self.op_map['^']), r+1, 1, color='#FFC107')


    def number_click(self, number):
        """Handles number and decimal point clicks."""
        self.current_input += str(number)
        self.update_display(self.current_input)

    def clear_display(self):
        """Clears the display and resets the calculator state."""
        self.current_input = ""
        self.first_operand = None
        self.pending_operation = None
        self.update_display("")

    def update_display(self, text):
        """Updates the Tkinter Entry widget."""
        self.display.delete(0, tk.END)
        self.display.insert(0, text)

    def operator_click(self, op_code):
        """Handles basic operator clicks (+, -, *, /)."""
        try:
            # If an operation is already pending, calculate the intermediate result
            if self.first_operand is not None and self.pending_operation is not None and self.current_input:
                self.calculate()
                
            # Store the current input as the first operand
            self.first_operand = float(self.current_input)
            self.pending_operation = op_code
            self.current_input = ""
            self.update_display(str(self.first_operand)) # Display the first operand temporarily

        except ValueError:
            messagebox.showerror("Error", "Invalid number input.")
            self.clear_display()

    def calculate(self):
        """Performs the final calculation for basic operations."""
        if self.first_operand is None or self.pending_operation is None or not self.current_input:
            return

        try:
            number2 = float(self.current_input)
            result = calculator.basic_operations(self.first_operand, number2, self.pending_operation)
            
            # Construct calculation string for history
            op_symbol = {v: k for k, v in self.op_map.items()}[self.pending_operation]
            calc_string = f"{self.first_operand} {op_symbol} {number2}"
            self.history = history_manager.add_to_history(self.history, calc_string, result)
            
            self.update_display(str(result))
            self.first_operand = result
            self.pending_operation = None
            self.current_input = str(result) # Allow chaining operations

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation Error: {e}")
            
    # --- History Management Methods ---

    def show_history(self):
        """Opens a new window to display calculation history."""
        history_window = tk.Toplevel(self.master)
        history_window.title("Calculation History")
        
        listbox = tk.Listbox(history_window, width=50, height=20, font=('Arial', 10))
        listbox.pack(padx=10, pady=10)
        
        if not self.history:
            listbox.insert(tk.END, "No history recorded yet.")
        else:
            for item in reversed(self.history): # Show newest first
                listbox.insert(tk.END, item)
                
        def copy_result():
            """Copies the result of the selected history entry to the main display."""
            try:
                selected_index = listbox.curselection()[0]
                selected_text = listbox.get(selected_index)
                # Extract the result (part after ' = ')
                result_str = selected_text.split(' = ')[-1]
                self.clear_display()
                self.number_click(result_str)
                history_window.destroy()
            except IndexError:
                messagebox.showwarning("Warning", "Please select a history entry.")
            except Exception:
                messagebox.showerror("Error", "Could not parse result.")

        copy_btn = tk.Button(history_window, text="Copy Result to Calculator", command=copy_result)
        copy_btn.pack(pady=5)

    def on_close(self):
        """Saves history and closes the application."""
        history_manager.save_history(self.history)
        self.master.destroy()

    # --- Advanced Function Menu ---

    def show_advanced_menu(self):
        """Opens a new window for advanced function evaluation."""
        adv_window = tk.Toplevel(self.master)
        adv_window.title("Advanced Functions")
        
        # Display the current main input for clarity
        tk.Label(adv_window, text=f"Current Main Input (x): {self.current_input}", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Function-specific entry for power/root (number2_optional)
        tk.Label(adv_window, text="Optional Secondary Input (y for x^y or x^(1/y)):").pack(pady=2)
        secondary_input = tk.Entry(adv_window, width=15)
        secondary_input.pack(pady=5)
        
        
        # Function Buttons Setup
        func_options = [
            ("Power (x^y)", 1), ("Root (x^(1/y))", 2), ("Reciprocal (1/x)", 3), ("Exponential (e^x)", 4),
            ("ln(x)", 5), ("log10(x)", 6), ("log2(x)", 7), ("sin(x°)", 8),
            ("cos(x°)", 9), ("tan(x°)", 10), ("asin(x)", 11), ("acos(x)", 12),
            ("atan(x)", 13), ("Factorial (n!)", 14), ("Constants ($\pi$/e - input 1 or 2 in x)", 15)
        ]

        def evaluate_function(op_code, op_name):
            """Calls the function_eval with current inputs."""
            try:
                # Primary Input (number1)
                num1 = float(self.current_input)
                
                # Secondary Input (number2_optional)
                num2_opt_str = secondary_input.get()
                num2_opt = float(num2_opt_str) if num2_opt_str else None
                
                result = calculator.function_eval(num1, op_code, num2_opt)
                
                # Construct calculation string for history
                if op_code in [1, 2]:
                    op_sym = op_name.split('(')[0] # Extract Power or Root
                    calc_string = f"{num1} {op_sym} {num2_opt}"
                elif op_code == 15:
                    const_name = "$\pi$" if num1 == 1 else "$e$"
                    calc_string = f"{op_name}: {const_name}"
                elif op_code == 14:
                     calc_string = f"Factorial({int(num1)})"
                else:
                    calc_string = f"{op_name}({num1})"

                self.history = history_manager.add_to_history(self.history, calc_string, result)
                
                self.update_display(str(result))
                adv_window.destroy()

            except ValueError as e:
                messagebox.showerror("Function Error", str(e))
            except Exception as e:
                messagebox.showerror("Function Error", f"An unexpected error occurred: {e}")


        # Create and grid the function buttons
        func_frame = tk.Frame(adv_window)
        func_frame.pack(padx=10, pady=10)
        
        row, col = 0, 0
        for name, code in func_options:
            btn = tk.Button(func_frame, text=name, command=lambda c=code, n=name: evaluate_function(c, n), padx=5, pady=5)
            btn.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
            col += 1
            if col > 3: # 4 buttons per row
                col = 0
                row += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()