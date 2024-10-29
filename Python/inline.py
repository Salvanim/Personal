import re

def extract_functions(code_text):
    # Extract function definitions using regex
    func_pattern = r'(?P<name>\w+)\((?P<params>[^)]*)\):\s*(?P<body>.*?)\n(?=\s*\w|\Z)'
    functions = {}

    for match in re.finditer(func_pattern, code_text, re.DOTALL):
        name = match.group('name')
        params = match.group('params').strip().split(',')
        body = match.group('body').strip()
        functions[name] = (params, body)

    return functions

def replace_inline_functions(code_text, functions):
    # Create a regex pattern to match function calls
    call_pattern = r'\b(' + '|'.join(re.escape(func) for func in functions.keys()) + r')\s*\(([^)]*)\)'

    # Replace inline function calls with their bodies
    modified_code = code_text

    # Find all function calls and replace them
    for match in re.finditer(call_pattern, modified_code):
        func_name = match.group(1)
        args = match.group(2).strip().split(',')

        if func_name not in functions:
            continue  # Skip if function is not found

        param_names, body = functions[func_name]
        arg_dict = {param.strip(): arg.strip() for param, arg in zip(param_names, args)}

        # Replace parameters with actual arguments in the function body
        for param, arg in arg_dict.items():
            body = body.replace(param, arg)

        # Remove the 'return' keyword if present
        body = body.replace('return ', '')  # Remove 'return ' from the body
        body = body.strip()  # Strip any extra whitespace

        # Replace the function call with the body
        modified_code = modified_code.replace(match.group(0), f"({body})")  # Replace the whole function call

    return modified_code

# Example usage
if __name__ == "__main__":
    # Sample code with inline functions defined
    sample_code = """
    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y

    def combine(a, b):
        return add(a, b) + subtract(a, b)

    result1 = add(5, 3)
    result2 = subtract(10, 4)
    result3 = combine(10, 5)
    """

    # Extract functions from the code
    functions = extract_functions(sample_code)

    # Replace inline functions with their body
    modified_code = replace_inline_functions(sample_code, functions)

    print("Modified Code:\n", modified_code)
