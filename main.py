import calculator

def deciding_operation():
    while True:
        print("\nPick an option:\n\n1. Select a number (Basic Operations)\n\n2. Select a function (Function Evaluation)")
        
        # Robust input for the main menu option
        try:
            option1 = int(input("\nOption: "))
        except ValueError:
            print("\nInvalid input. Please enter a valid option number (1 or 2).")
            continue
            
        if option1 not in {1,2}:
            print("\nYou have to select a valid option between the two possible ones, try again...")
        else:
            break
    return option1

def main():
    option1 = deciding_operation()

    if option1 == 1:
        print(f"\nThe result of performing those operations is {calculator.basic_operations()}")
    else:
        print(f"\nThe result of performing those operations is {calculator.function_eval()}")

if __name__ == "__main__":
    main()