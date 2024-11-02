import re
import os
import requests

def get_package_from_pypi(import_name):
    response = requests.get(f'https://pypi.org/pypi/{import_name}/json')
    if response.status_code == 200:
        return import_name  # The name matches the package
    else:
        # Attempt a search for similar names if the exact name isn't found
        search_response = requests.get(f'https://pypi.org/pypi?name={import_name}')
        if search_response.ok:
            packages = search_response.json().get('hits', {}).get('hits', [])
            if packages:
                return packages[0]['name']  # Return the first search result
    return None

def extract_imports():
    file_path = os.path.abspath(__file__)
    imports = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Match import statements (standard import and from-import)
                if re.match(r'^\s*(import|from)\s+', line):
                    imports.append(f"pip install {get_package_from_pypi(line.strip().split("import ")[1])}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    return imports


file_path = os.path.abspath(__file__)
imports = extract_imports()
print(imports)

