import tkinter as tk
from tkinter import messagebox
import calculator
import history_manager

class CalculatorGUI:
    # --- Aesthetic Configuration ---
    COLOR_BG = '#282C34'       # Dark background
    COLOR_OP = '#FF9F0A'       # Orange accent for operators
    COLOR_NUM = '#4F5560'      # Darker grey for numbers
    COLOR_AC = '#A2A2A2'       # Light grey for general controls
    COLOR_TXT = 'white'        # Default text color
    COLOR_DISPLAY_BG = '#3A3F48' # Slightly lighter dark for display

    def __init__(self, master):
        self.master = master
        master.title("Advanced Python Calculator")
        master.configure(bg=self.COLOR_BG)
        
        # Configure grid weights to make buttons expand evenly
        for i in range(6): 
            master.grid_columnconfigure(i, weight=1)
        for i in range(7):
            master.grid_rowconfigure(i, weight=1)

        # --- History Management ---
        self.history = history_manager.load_history()

        # --- State Variables ---
        self.current_input = ""
        self.first_operand = None
        self.pending_operation = None # Stores the option code for basic_operations

        # --- UI Setup ---
        
        # 1. Display
        self.display = tk.Entry(
            master, 
            width=20, 
            borderwidth=0, 
            font=('Arial', 32), # Large, readable font
            justify='right',
            bg=self.COLOR_DISPLAY_BG, 
            fg=self.COLOR_TXT,
            relief='flat', 
            insertbackground=self.COLOR_TXT
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=15, sticky="ew")

        # 2. Buttons (Numbers and Basic Ops)
        self.create_buttons()

        # 3. History Button
        self.create_btn("History", lambda: self.show_history(), 1, 4, color=self.COLOR_AC, fg='black')
        
        # 4. Advanced Functions Button
        self.create_btn("Functions", lambda: self.show_advanced_menu(), 2, 4, color=self.COLOR_AC, fg='black')
        
        # Configure closing protocol to save history
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_btn(self, text, command, row, col, columnspan=1, color=None, fg=None):
        """Helper function to create and place an aesthetic button."""
        if color is None:
            color = self.COLOR_NUM
        if fg is None:
            fg = self.COLOR_TXT

        button = tk.Button(
            self.master, 
            text=text, 
            padx=10, 
            pady=10, 
            command=command, 
            bg=color, 
            fg=fg, 
            font=('Arial', 14),
            borderwidth=0, 
            relief='flat', # Flat look
            activebackground=self.COLOR_AC # Feedback color when pressed
        )
        button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=4, pady=4)
        return button

    def create_buttons(self):
        """Creates number, operator, and special buttons."""
        
        # Basic Operation map for calculator.basic_operations()
        self.op_map = {'+': 1, '-': 2, '*': 3, '/': 4, '%': 5, '^': 6}
        
        # Button layout: (text, row, col, color)
        buttons = [
            ('7', 1, 0, self.COLOR_NUM), ('8', 1, 1, self.COLOR_NUM), ('9', 1, 2, self.COLOR_NUM), ('/', 1, 3, self.COLOR_OP),
            ('4', 2, 0, self.COLOR_NUM), ('5', 2, 1, self.COLOR_NUM), ('6', 2, 2, self.COLOR_NUM), ('*', 2, 3, self.COLOR_OP),
            ('1', 3, 0, self.COLOR_NUM), ('2', 3, 1, self.COLOR_NUM), ('3', 3, 2, self.COLOR_NUM), ('-', 3, 3, self.COLOR_OP),
            ('0', 4, 0, self.COLOR_NUM), ('.', 4, 1, self.COLOR_NUM), ('C', 4, 2, 'red'), ('+', 4, 3, self.COLOR_OP),
            ('%', 5, 0, self.COLOR_OP), ('^', 5, 1, self.COLOR_OP), ('=', 5, 2, 'green', 2)
        ]
        
        for (text, row, col, color, *cs) in buttons:
            columnspan = cs[0] if cs else 1
            
            if text.isdigit() or text == '.':
                self.create_btn(text, lambda t=text: self.number_click(t), row, col, color=color)
            elif text in self.op_map:
                op_code = self.op_map[text]
                self.create_btn(text, lambda op=op_code: self.operator_click(op), row, col, color=color)
            elif text == 'C':
                self.create_btn(text, self.clear_display, row, col, color=color)
            elif text == '=':
                self.create_btn(text, self.calculate, row, col, columnspan=columnspan, color=color)

    # --- UI Logic ---

    def number_click(self, number):
        """Handles number and decimal point clicks."""
        # Prevent multiple decimals unless cleared
        if number == '.' and '.' in self.current_input:
            return
            
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
        """Handles basic operator clicks."""
        try:
            # If input is empty, try to use the last result as the first operand
            if not self.current_input and self.first_operand is not None:
                # Use existing first_operand, no need to parse input
                pass
            elif self.current_input:
                # If an operation is already pending, calculate the intermediate result
                if self.first_operand is not None and self.pending_operation is not None:
                    self.calculate()
                    
                # Store the current input as the first operand
                self.first_operand = float(self.current_input)
                self.update_display(str(self.first_operand)) # Display the first operand temporarily
            
            self.pending_operation = op_code
            self.current_input = ""

        except ValueError:
            messagebox.showerror("Error", "Invalid number input for operation.")
            self.clear_display()

    def calculate(self):
        """Performs the final calculation for basic operations."""
        if self.first_operand is None or self.pending_operation is None:
            return

        # Use the current input as the second operand
        try:
            number2 = float(self.current_input)
        except ValueError:
            messagebox.showerror("Error", "Invalid second number input.")
            return

        try:
            result = calculator.basic_operations(self.first_operand, number2, self.pending_operation)
            
            # Construct calculation string for history
            op_symbol = {v: k for k, v in self.op_map.items()}[self.pending_operation]
            calc_string = f"{self.first_operand} {op_symbol} {number2}"
            self.history = history_manager.add_to_history(self.history, calc_string, result)
            
            self.update_display(str(result))
            
            # Reset state for next chained operation
            self.first_operand = result
            self.pending_operation = None
            self.current_input = str(result) # Allow chaining operations

        except ValueError as e:
            messagebox.showerror("Math Error", str(e))
            self.clear_display()
        except Exception as e:
            messagebox.showerror("Error", f"Calculation Error: {e}")
            self.clear_display()
            
    # --- History Management Methods ---

    def show_history(self):
        """Opens a new window to display calculation history."""
        history_window = tk.Toplevel(self.master, bg=self.COLOR_BG)
        history_window.title("Calculation History")
        
        listbox = tk.Listbox(history_window, width=50, height=20, font=('Arial', 10), 
                             bg=self.COLOR_DISPLAY_BG, fg=self.COLOR_TXT, selectbackground=self.COLOR_OP)
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

        copy_btn = tk.Button(history_window, text="Copy Result to Calculator", command=copy_result, 
                             bg=self.COLOR_OP, fg=self.COLOR_TXT, font=('Arial', 12), relief='flat')
        copy_btn.pack(pady=5, padx=10, fill='x')

    def on_close(self):
        """Saves history and closes the application."""
        history_manager.save_history(self.history)
        self.master.destroy()

    # --- Advanced Function Menu ---

    def show_advanced_menu(self):
        """Opens a new window for advanced function evaluation."""
        adv_window = tk.Toplevel(self.master, bg=self.COLOR_BG)
        adv_window.title("Advanced Functions")
        
        # Frame for inputs
        input_frame = tk.Frame(adv_window, bg=self.COLOR_BG)
        input_frame.pack(pady=10, padx=10, fill='x')

        # Primary Input (x)
        tk.Label(input_frame, text="Input X:", bg=self.COLOR_BG, fg=self.COLOR_TXT, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        # Display the current main input for clarity
        current_input_label = tk.Label(input_frame, text=self.current_input if self.current_input else "0", 
                                       bg=self.COLOR_DISPLAY_BG, fg=self.COLOR_TXT, font=('Arial', 12, 'bold'), width=10)
        current_input_label.pack(side=tk.LEFT, padx=10)
        
        # Secondary Input (y)
        tk.Label(input_frame, text="Input Y (for x^y, root):", bg=self.COLOR_BG, fg=self.COLOR_TXT, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        secondary_input = tk.Entry(input_frame, width=10, bg=self.COLOR_DISPLAY_BG, fg=self.COLOR_TXT, font=('Arial', 12))
        secondary_input.pack(side=tk.LEFT, padx=5)
        
        
        # Function Buttons Setup
        func_options = [
            ("Power (x^y)", 1), ("Root (x^(1/y))", 2), ("Reciprocal (1/x)", 3), ("Exponential (e^x)", 4),
            ("ln(x)", 5), ("log10(x)", 6), ("log2(x)", 7), ("sin(x°)", 8),
            ("cos(x°)", 9), ("tan(x°)", 10), ("asin(x)", 11), ("acos(x)", 12),
            ("atan(x)", 13), ("Factorial (n!)", 14), ("Constants ($\pi$/e)", 15)
        ]

        def evaluate_function(op_code, op_name):
            """Calls the function_eval with current inputs."""
            try:
                # Primary Input (number1)
                num1_str = current_input_label.cget("text")
                if not num1_str or num1_str == "0":
                    raise ValueError("Primary input (x) is required.")
                num1 = float(num1_str)
                
                # Secondary Input (number2_optional)
                num2_opt_str = secondary_input.get()
                num2_opt = float(num2_opt_str) if num2_opt_str else None
                
                result = calculator.function_eval(num1, op_code, num2_opt)
                
                # Construct calculation string for history
                if op_code == 1:
                    calc_string = f"pow({num1}, {num2_opt})"
                elif op_code == 2:
                    calc_string = f"root({num1}, {num2_opt})"
                elif op_code == 15:
                    const_name = "Pi ($\pi$)" if num1 == 1 else "Euler ($e$)"
                    calc_string = f"{const_name}"
                elif op_code == 14:
                     calc_string = f"Factorial({int(num1)})"
                else:
                    calc_string = f"{op_name.split('(')[0]}({num1})"

                self.history = history_manager.add_to_history(self.history, calc_string, result)
                
                self.update_display(str(result))
                adv_window.destroy()

            except ValueError as e:
                messagebox.showerror("Function Error", str(e))
            except Exception as e:
                messagebox.showerror("Function Error", f"An unexpected error occurred: {e}")


        # Create and grid the function buttons
        func_frame = tk.Frame(adv_window, bg=self.COLOR_BG)
        func_frame.pack(padx=10, pady=10)
        
        row, col = 0, 0
        for name, code in func_options:
            btn = tk.Button(func_frame, text=name, command=lambda c=code, n=name: evaluate_function(c, n), 
                            padx=5, pady=5, bg=self.COLOR_NUM, fg=self.COLOR_TXT, font=('Arial', 12), relief='flat')
            btn.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            col += 1
            if col > 3: # 4 buttons per row
                col = 0
                row += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()