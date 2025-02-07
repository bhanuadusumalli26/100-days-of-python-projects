import os

def clear():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
logo='''
_____________________
|  _________________  |
| | JO           0. | |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|
 
 '''
print(logo)
def add(n1,n2):
    return n1+n2
def sub(n1,n2):
    return n1-n2
def mul(n1,n2):
    return n1*n2
def divide(n1,n2):
    return n1/n2
operation={ "+":add,
           "-":sub,
           "*":mul,
           "/":divide}
def calculator():
    num1=float(input("What's the First number?:"))
    for symbol in operation:
        print(symbol)
    should_continue=True    
    while should_continue:
        operation_symbol = input("Pick an operation: ")
        num2 = float(input("What's the next number?: "))
        calculation_function = operation[operation_symbol]
        answer = calculation_function(num1, num2)
        print(f"{num1} {operation_symbol} {num2} = {answer}")
        if input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ") == 'y':
           num1 = answer
        else:
            should_continue = False
            clear()
            calculator()
calculator()

