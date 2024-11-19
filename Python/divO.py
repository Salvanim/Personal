import math

# Define OType class with custom behavior
class OType:
    def __init__(self, type_name="O"):
        self.type_name = type_name

    def __repr__(self):
        return f"{self.type_name}"

    # Define behavior for O + O
    def __add__(self, other):
        if isinstance(other, OType):
            return OType("O")  # O + O = O
        elif isinstance(other, (int, float)):
            return OType("O")  # Adding a number to O still results in O type
        elif isinstance(other, ImaginaryUnit):
            return "O + i"  # Custom interaction with i
        else:
            return NotImplemented

    # Define behavior for O - O
    def __sub__(self, other):
        if isinstance(other, OType):
            return OType("O")  # O - O = O
        elif isinstance(other, (int, float)):
            return OType("O")  # Subtracting a number still results in O
        elif isinstance(other, ImaginaryUnit):
            return "O - i"  # Custom interaction with i
        else:
            return NotImplemented

    # Define behavior for O * O or x * O
    def __mul__(self, other):
        if isinstance(other, OType):
            return OType("O")  # O * O = O
        elif isinstance(other, (int, float)):
            return OType("O")  # Any number * O = O
        elif isinstance(other, ImaginaryUnit):
            return "O * i"  # Custom interaction with i
        else:
            return NotImplemented

    # Define behavior for O / O or x / O
    def __truediv__(self, other):
        if isinstance(other, OType):
            return OType("O")  # O / O = O
        elif isinstance(other, (int, float)) and other == 0:
            return OType("O")  # Division by 0 gives x * O
        elif isinstance(other, ImaginaryUnit):
            return "O / i"  # Custom interaction with i
        else:
            return NotImplemented

    # Define exponentiation behavior: O^O = O_o, etc.
    def __pow__(self, other):
        if isinstance(other, OType):
            return OType("O_o")  # O^O = O_o
        elif isinstance(other, (int, float)):
            return OType("O")  # O^n, for n >= 2, results in O
        else:
            return NotImplemented

    # Define logarithm behavior: log(O) = O - O
    def log(self):
        return OType("O-")  # log(O) = O - O (negative O)

    # Factorial behavior for O
    def factorial(self):
        return "O!"  # Placeholder for factorial logic


# Define imaginary unit (i)
class ImaginaryUnit:
    def __repr__(self):
        return "i"

    def __mul__(self, other):
        if isinstance(other, OType):
            return OType("O_i")  # O * i = O_i
        elif isinstance(other, (int, float)):
            return f"i * {other}"  # i * normal number
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return f"{other} + i"  # normal number + i
        elif isinstance(other, OType):
            return "O + i"  # Custom interaction with O
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return f"{other} - i"  # normal number - i
        elif isinstance(other, OType):
            return "O - i"  # Custom interaction with O
        else:
            return NotImplemented


class MathInterpreter:
    def __init__(self):
        self.O = OType()  # This creates an instance of the OType class
        self.i = ImaginaryUnit()  # This creates an instance of the ImaginaryUnit class

    def parse(self, expression):
        # Handle log(O) and O! directly by checking for 'O' or 'i' in the operation
        if "log(" in expression:
            # If O or i are present, use custom log; otherwise, use math.log
            expression = expression.replace("log(", "math.log(")

        if "!" in expression:
            # If O is involved, use custom factorial; otherwise, use math.factorial
            expression = expression.replace("!", "math.factorial(") + ")"

        # Define custom syntax for O and i, replacing them with our classes
        expression = expression.replace('O', 'self.O')
        expression = expression.replace('i', 'self.i')
        expression = expression.replace('^', '**')
        # Evaluate the expression safely using the self object in globals
        try:
            # Ensuring that the object references (self.O, self.i) are used properly for operations
            result = eval(expression, {"self": self})
            return result
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"


# Test the interpreter
def test_interpreter():
    interpreter = MathInterpreter()

    # Define test expressions
    test_expressions = [
        "O + O",
        "O * O",
        "i + 5",
        "i * 5",
        "O / i",
        "O + 5",
        "O * 5",
        "O ^ O",
        "log(O)",
        "log(100)",
        "O! + 2 * i",
        "i + O",
        "i - 5"
    ]

    # Evaluate and print results
    for expr in test_expressions:
        print(f"{expr} = {interpreter.parse(expr)}")


# Run the tests
test_interpreter()

