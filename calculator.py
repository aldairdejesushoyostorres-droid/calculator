import math

def basic_operations():
    # Robust input for the first number
    while True:
        try:
            number1 = float(input("\nWrite a number: "))
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
    while True:
        print("\nHow do you want to operate this number:")
        print("\n1. Add it to another number")
        print("\n2. Subtract it to another number")
        print("\n3. Multiply it to another number")
        print("\n4. Divide it to another number")
        print("\n5. Modulo (remainder) it to another number")
        print("\n6. Raise it to the power of another number")

        # Robust input for the operation option
        try:
            option2 = int(input("\nOption: "))
        except ValueError:
            print("\nInvalid input. Please enter a valid option number (1-6).")
            continue

        if option2 not in {1, 2, 3, 4, 5, 6}:
            print("\nYou have to select a valid option between the possible ones, try again...")
        else:
            # Robust input for the second number
            while True:
                try:
                    number2 = float(input("\nWrite a second number: "))
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

            match option2:
                case 1:
                    output = number1 + number2
                case 2:
                    output = number1 - number2
                case 3:
                    output = number1 * number2
                case 4:
                    while True:
                        if number2 == 0:
                            number2 = float(input("\nYou can't divide by zero, pick another number: "))
                        else:
                            break
                    output = number1 / number2
                case 5:
                    while True:
                        if number2 == 0:
                            number2 = float(input("\nYou can't perform modulo with zero, pick another number: "))
                        else:
                            break
                    output = number1 % number2
                case 6:
                    output = pow(number1, number2)
            break
    # Rounding for cleaner output
    return round(output, 6)

def function_eval():
    while True:
        print("\nSelect any of the following functions: ")
        print("\n1. Power (x^y)")
        print("\n2. Root (x^(1/y))")
        print("\n3. Reciprocal (1/x)")
        print("\n4. Exponential (e^x)")
        print("\n5. Natural Logarithm (ln(x))")
        print("\n6. Logarithm Base 10 (log10(x))")
        print("\n7. Logarithm Base 2 (log2(x))")
        print("\n8. Sine (sin(x) - input in degrees)")
        print("\n9. Cosine (cos(x) - input in degrees)")
        print("\n10. Tangent (tan(x) - input in degrees)")
        print("\n11. Arcsine (asin(x))")
        print("\n12. Arccosine (acos(x))")
        print("\n13. Arctangent (atan(x))")
        print("\n14. Factorial (n!)")
        print("\n15. Math Constants ($\pi$ or $e$ output)")

        # Robust input for the operation option
        try:
            option2 = int(input("\nOption: "))
        except ValueError:
            print("\nInvalid input. Please enter a valid option number (1-15).")
            continue

        if option2 <= 0 or option2 >= 16:
            print("\nYou have to select a valid option among the ones provided")
        elif option2 == 15: # Constants Case
            print("\n1. Pi ($\pi$)")
            print("\n2. Euler's Number ($e$)")
            while True:
                try:
                    const_option = int(input("\nPick a constant: "))
                    if const_option == 1:
                        output = math.pi
                    elif const_option == 2:
                        output = math.e
                    else:
                        print("\nInvalid constant option.")
                        continue
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a number.")
            break
        else:
            # Robust input for the number input into the function
            while True:
                try:
                    number1 = float(input("\nWrite a number to be input into the function: "))
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")

            match option2:
                case 1:
                    while True:
                        try:
                            power = float(input("\nPick the power you want to raise your number to: "))
                            break
                        except ValueError:
                            print("\nInvalid input. Please enter a valid number.")
                    output = pow(number1, power)
                case 2:
                    while True:
                        try:
                            root = float(input("\nPick the root (e.g., 2 for square root, 3 for cube root): "))
                            if root == 0:
                                print("\nRoot cannot be zero.")
                                continue
                            break
                        except ValueError:
                            print("\nInvalid input. Please enter a valid number.")
                    output = pow(number1, 1/root)
                case 3:
                    while True:
                        if number1 == 0:
                            number1 = float(input("\nWe can't perform the reciprocal of zero, pick another number: "))
                        else:
                            break
                    output = 1/number1
                case 4:
                    output = math.exp(number1)
                case 5:
                    output = math.log(number1) # Natural Log
                case 6:
                    output = math.log10(number1)
                case 7:
                    output = math.log2(number1)
                case 8:
                    output = math.sin(math.radians(number1)) # Convert degrees to radians
                case 9:
                    output = math.cos(math.radians(number1)) # Convert degrees to radians
                case 10:
                    output = math.tan(math.radians(number1)) # Convert degrees to radians
                case 11:
                    output = math.asin(number1)
                case 12:
                    output = math.acos(number1)
                case 13:
                    output = math.atan(number1)
                case 14:
                    # Factorial check for non-negative integers
                    if number1 < 0 or number1 != int(number1):
                        print("\nFactorial is only defined for non-negative integers.")
                        output = "ERROR: Factorial not defined" # Set error message
                    else:
                        output = math.factorial(int(number1))
            break
    
    # Check if output is a number before rounding
    if isinstance(output, (int, float)):
        return round(output, 6)
    else:
        return output