import os
import ast


def find_imports(file_path):
    with open(file_path) as f:
        node = ast.parse(f.read())

    imports = []
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            imports += [alias.name for alias in n.names]
        elif isinstance(n, ast.ImportFrom):
            module_name = n.module if n.module else ""
            imports += [f"{module_name}.{alias.name}" for alias in n.names]

    return imports


folder_path = r"recup_st_reader\src"
all_imports = set()

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            imports = find_imports(file_path)
            all_imports.update(imports)

print(all_imports)
