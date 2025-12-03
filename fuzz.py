import random
import string
import traceback
import ast
import os
import sys

sys.path.append("MLForensics/MLForensics_farzana/FAME-ML")

# Import the modules
import py_parser
import constants

BUG_REPORT_FILE = "4a_fuzz_report.txt"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def random_ast_node():
    """Generate a random AST node (may or may not be valid)."""
    node_types = [ast.Call, ast.Name, ast.Attribute, ast.Assign, ast.Expr]
    node_type = random.choice(node_types)
    try:
        if node_type == ast.Call:
            return ast.Call(
                func=ast.Name(id=random_string(), ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        elif node_type == ast.Name:
            return ast.Name(id=random_string(), ctx=ast.Load())
        elif node_type == ast.Attribute:
            return ast.Attribute(
                value=ast.Name(id=random_string(), ctx=ast.Load()),
                attr=random_string(),
                ctx=ast.Load()
            )
        elif node_type == ast.Assign:
            return ast.Assign(
                targets=[ast.Name(id=random_string(), ctx=ast.Store())],
                value=ast.Constant(value=random_string())
            )
        elif node_type == ast.Expr:
            return ast.Expr(value=ast.Constant(value=random_string()))
    except Exception:
        return None

def fuzz_function(func, trials=50):
    """Fuzz a function with random inputs."""
    with open(BUG_REPORT_FILE, "a") as f:
        for i in range(trials):
            try:
                if func.__name__ == "getPythonParseObject":
                    
                    fake_path = "/tmp/" + random_string() + ".py"
                    func(fake_path)
                elif func.__name__ in ["commonAttribCallBody", "getFunctionAssignments",
                                       "getPythonAtrributeFuncs", "getFunctionDefinitions"]:
                    # Provide random AST nodes
                    node = random_ast_node()
                    if node is None:
                        continue
                    func(node)
            except Exception as e:
                f.write(f"Function {func.__name__} crashed on trial {i}:\n")
                f.write(traceback.format_exc())
                f.write("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    # Clear previous bug report
    if os.path.exists(BUG_REPORT_FILE):
        os.remove(BUG_REPORT_FILE)

    functions_to_fuzz = [
        py_parser.getPythonParseObject,
        py_parser.commonAttribCallBody,
        py_parser.getFunctionAssignments,
        py_parser.getPythonAtrributeFuncs,
        py_parser.getFunctionDefinitions
    ]

    for func in functions_to_fuzz:
        fuzz_function(func)

    print(f"Fuzzing complete. Check {BUG_REPORT_FILE} for any crashes found.")
