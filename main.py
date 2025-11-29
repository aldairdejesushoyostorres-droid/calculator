import calculator

option1 = calculator.deciding_operation()

if option1 == 1:
    print(f"\nThe result of performing those operations is {calculator.basic_operations()}")
else:
    print(f"\nThe result of performing those operations is {calculator.function_eval()}")