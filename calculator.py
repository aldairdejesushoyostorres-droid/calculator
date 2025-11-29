def deciding_operation():
    while True:
        print("\nPick an option:\n\n1. Select a number\n\n2. Select a function")
        option1 = int(input("\nOption: "))
        if option1 not in {1,2}:
            print("\nYou have to select a valid option between the two possible ones, try again...")
        else:
            break
    return option1

def basic_operations():
    number1 = float(input("\nWrite a number: "))
    while True:
        print("\nHow do you want to operate this number:")
        print("\n1. Add it to another number") 
        print("\n2. Subtract it to another number") 
        print("\n3. Multiply it to another number") 
        print("\n4. Divide it to another number")
        option2 = int(input("\nOption: "))
        if option2 not in {1,2,3,4}:
            print("\nYou have to select a valid option between the four possible ones, try again...")
        else:
            number2 = float(input("\nWrite a number: "))
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
            break
    return output

def function_eval():
    import math
    while True:
        print("\nSelect any of the following functions: ")
        print("\n1. Power")
        print("\n2. Root")
        print("\n3. Reciprocal")
        print("\n4. Exponential")
        print("\n5. Natural Logarithm")
        print("\n6. Sine")
        print("\n7. Cosine")
        print("\n8. Tangent")
        print("\n9. Factorial")
        option2 = int(input("\nOption: "))
        if option2 <= 0 or option2 >= 10:
            print("\nYou have to select a valid option among the ones provided")
        else:
            number1 = float(input("\nWrite a number to be input into the function: "))
            match option2:
                case 1:
                    power = int(input("\nPick the power you want to raise your number to: "))
                    output = pow(number1,power)
                case 2:
                    root = int(input("\nPick the root you want to raise your number to: "))
                    output = pow(number1,1/root)
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
                    output = math.log(number1)
                case 6:
                    output = math.sin(number1)
                case 7:
                    output = math.cos(number1)
                case 8:
                    output = math.tan(number1)
                case 9:
                    output = 1
                    for i in range(1,int(number1)+1):
                        output *= i
            break
    return output