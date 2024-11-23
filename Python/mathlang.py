import math
import ast

class MathLangInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def evaluate(self, expression):
        if '=' in expression:
            var_name, value_str = expression.split('=', 1)
            var_name = var_name.strip()
            value_str = value_str.strip()
            if var_name.__contains__("("):
                
            try:
                value = ast.literal_eval(value_str)
                if (type(value) != int) and (type(value) != list):
                    raise TypeError(f"Invalid Value {value_str}")
            except (ValueError, SyntaxError) as e:
                value = (str(value_str), "expression")

            self.variables[var_name] = value
            return var_name, value
        return False


Other = MathLangInterpreter()
Other.evaluate("test = 1")
print(Other.variables['test'])
