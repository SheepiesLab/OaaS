import ast

source = ''
with open('account.py', 'r') as f:
    source = f.read()


module_tree = ast.parse(source, 'account.py')
for i in module_tree.body:
    if isinstance(i, ast.ClassDef) or isinstance(i, ast.FunctionDef):
        print(ast.dump(i, indent=2))