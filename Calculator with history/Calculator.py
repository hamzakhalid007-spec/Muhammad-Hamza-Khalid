import datetime
import math

HISTORY_FILE = "history.txt"

# Mathematical constants
CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'phi': (1 + math.sqrt(5)) / 2  # Golden ratio
}

def show_history():
    try:
        file = open(HISTORY_FILE, 'r')
        lines = file.readlines()
        file.close()
        if len(lines) == 0:
            print("No history found.")
        else:
            for line in reversed(lines):
                print(line.strip())
    except FileNotFoundError:
        print("No history found.")

def clear_history():
    file = open(HISTORY_FILE, 'w')
    file.close()
    print("History cleared.")

def evaluate_expression(expression):
    """Evaluate mathematical expressions with functions and constants"""
    try:
        # Replace constants
        for const, value in CONSTANTS.items():
            expression = expression.replace(const, str(value))
        
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        
        # Create safe namespace for eval with math functions
        safe_dict = {
            "__builtins__": {},
            # Basic math functions
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "abs": abs,
            "round": round,
            "floor": math.floor,
            "ceil": math.ceil,
            "pow": pow,
            # Constants (in case they're used as functions)
            "pi": math.pi,
            "e": math.e
        }
        
        result = eval(expression, safe_dict)
        
        # Convert to int if it's a whole number
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        return result
        
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def save_to_history(equation, result):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file = open(HISTORY_FILE, 'a')
        file.write(f"[{timestamp}] {equation} = {str(result)}\n")
        file.close()
    except Exception as e:
        print(f"Error saving to history: {e}")
    
def calculate(user_input):
    # First try to evaluate as a complex expression
    try:
        result = evaluate_expression(user_input)
        print("Result:", result)
        save_to_history(user_input, result)
        return
    except:
        pass
    
    # If that fails, try the original simple calculation method
    parts = user_input.split()
    if len(parts) < 3:
        print("Invalid input. Use format: number operator number (e.g 8 + 8)")
        print("Or try expressions like: sqrt(16), 2 + 3 * 4, sin(pi/2)")
        return
    
    try:
        num1 = float(parts[0])
        op = parts[1]
        num2 = float(parts[2])
        result = 0
        
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                print("Cannot divide by zero.")
                return
            result = num1 / num2
        elif op == '//':
            if num2 == 0:
                print("Cannot divide by zero.")
                return
            result = num1 // num2
        elif op == '%':
            if num2 == 0:
                print("Cannot divide by zero.")
                return
            result = num1 % num2
        elif op == '^':
            result = num1 ** num2
        else:
            print("Invalid operator.")
            return
        
        if int(result) == result:
            result = int(result)
        print("Result:", result)
        save_to_history(user_input, result)
        
    except ValueError:
        print("Invalid numbers in expression.")
    except Exception as e:
        print(f"Calculation error: {e}")

def show_help():
        """Display help information"""
        help_text = """
    --- Calculator Help ---

    Basic Operations:
    5 + 3, 10 - 2, 4 * 6, 15 / 3, 17 // 5, 17 % 5, 2 ^ 8

    Scientific Functions:
    sqrt(16), sin(pi/2), cos(0), tan(pi/4)
    log(e), log10(100), abs(-5), round(3.7)
    floor(3.9), ceil(3.1)

    Constants:
    pi = 3.14159..., e = 2.71828..., phi = 1.61803... (golden ratio)

    Complex Expressions:
    2 + 3 * 4
    sqrt(16) + sin(pi/2)
    (5 + 3) * 2
    2^3 + sqrt(9)

    Commands:
    history - show calculation history
    clear   - clear history
    help    - show this help
    exit    - quit calculator
        """
        print(help_text)

def main():
    print("----Welcome to Simple Calculator----\n")
    print("Type 'help' to see available functions and examples")
    while True:
        user_input = input("Enter equation or command: ").strip()
        if user_input == "exit":
            print("Goodbye.")
            break
        elif user_input == "history":
            show_history()
        elif user_input == "clear":
            clear_history()
        elif user_input == "help":
            show_help()
        elif user_input:  # Only process non-empty input
            calculate(user_input)
            
main()