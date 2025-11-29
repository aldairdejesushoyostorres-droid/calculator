import math
import json

# =========================================================================
# NOTE: These functions are modified to accept arguments instead of using
#       the input() function, making them callable from a GUI or history module.
# =========================================================================

def basic_operations(number1, number2, option2):
    """Performs basic arithmetic operations."""
    output = None
    
    match option2:
        case 1: # Add
            output = number1 + number2
        case 2: # Subtract
            output = number1 - number2
        case 3: # Multiply
            output = number1 * number2
        case 4: # Divide
            if number2 == 0:
                raise ValueError("Cannot divide by zero.")
            output = number1 / number2
        case 5: # Modulo
            if number2 == 0:
                raise ValueError("Cannot perform modulo with zero.")
            output = number1 % number2
        case 6: # Power
            output = pow(number1, number2)
        case _:
            raise ValueError("Invalid operation option.")
            
    # Rounding for cleaner output
    return round(output, 6)

def function_eval(number1, option2, number2_optional=None):
    """Evaluates a single-number function."""
    output = None
    
    match option2:
        case 1: # Power (number1 ^ number2)
            if number2_optional is None:
                raise ValueError("Power operation requires a second value.")
            output = pow(number1, number2_optional)
        case 2: # Root (number1 ^ (1/number2))
            if number2_optional is None:
                raise ValueError("Root operation requires a second value.")
            if number2_optional == 0:
                 raise ValueError("Root cannot be zero.")
            output = pow(number1, 1/number2_optional)
        case 3: # Reciprocal (1/number1)
            if number1 == 0:
                raise ValueError("Cannot perform reciprocal of zero.")
            output = 1/number1
        case 4: # Exponential (e^x)
            output = math.exp(number1)
        case 5: # Natural Logarithm (ln(x))
            if number1 <= 0:
                raise ValueError("Natural logarithm is only defined for positive numbers.")
            output = math.log(number1)
        case 6: # Logarithm Base 10 (log10(x))
            if number1 <= 0:
                raise ValueError("Logarithm Base 10 is only defined for positive numbers.")
            output = math.log10(number1)
        case 7: # Logarithm Base 2 (log2(x))
            if number1 <= 0:
                raise ValueError("Logarithm Base 2 is only defined for positive numbers.")
            output = math.log2(number1)
        case 8: # Sine (sin(x) - input in degrees)
            output = math.sin(math.radians(number1))
        case 9: # Cosine (cos(x) - input in degrees)
            output = math.cos(math.radians(number1))
        case 10: # Tangent (tan(x) - input in degrees)
            output = math.tan(math.radians(number1))
        case 11: # Arcsine (asin(x))
            if number1 < -1 or number1 > 1:
                raise ValueError("Arcsine input must be between -1 and 1.")
            output = math.asin(number1)
        case 12: # Arccosine (acos(x))
            if number1 < -1 or number1 > 1:
                raise ValueError("Arccosine input must be between -1 and 1.")
            output = math.acos(number1)
        case 13: # Arctangent (atan(x))
            output = math.atan(number1)
        case 14: # Factorial (n!)
            # Factorial check for non-negative integers
            if number1 < 0 or number1 != int(number1):
                raise ValueError("Factorial is only defined for non-negative integers.")
            output = math.factorial(int(number1))
        case 15: # Math Constants
            if number1 == 1:
                output = math.pi
            elif number1 == 2:
                output = math.e
            else:
                raise ValueError("Invalid constant option.")
        case _:
            raise ValueError("Invalid function option.")

    # Check if output is a number before rounding
    if isinstance(output, (int, float)):
        return round(output, 6)
    else:
        return output