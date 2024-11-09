import importlib
import dynamic  # Import dynamic.py initially

def add_function(function_code):
    """Appends generated function code to dynamic.py."""
    try:
        with open("dynamic.py", "a") as file:
            file.write("\n\n")  # Add spacing between functions for readability
            file.write(function_code)
        print("Function successfully added to dynamic.py")
    except Exception as e:
        print(f"Error adding function to dynamic.py: {e}")

def write_or_replace_function(function_code, function_name):
    """Writes or replaces a function in dynamic.py based on function_name."""
    try:
        with open("dynamic.py", "r") as file:
            lines = file.readlines()

        new_lines = []
        in_function = False
        for line in lines:
            # Start of function with the same name
            if line.startswith(f"def {function_name}("):
                in_function = True
            # Skip lines within the function to replace it
            if not in_function:
                new_lines.append(line)
            if in_function and line.strip() == "":
                in_function = False  # End of function

        # Add the new function at the end
        new_lines.append("\n\n")
        new_lines.append(function_code)

        # Write back to dynamic.py
        with open("dynamic.py", "w") as file:
            file.writelines(new_lines)
        print(f"Function {function_name} written to dynamic.py")
    except Exception as e:
        print(f"Error writing or replacing function in dynamic.py: {e}")

def load_dynamic_functions():
    """Reloads dynamic.py and returns a dictionary of functions."""
    try:
        importlib.reload(dynamic)
        # Retrieve all callable functions in dynamic
        functions = {name: getattr(dynamic, name) for name in dir(dynamic) if callable(getattr(dynamic, name))}
        print("Functions successfully loaded from dynamic.py")
        return functions
    except Exception as e:
        print(f"Error loading functions from dynamic.py: {e}")
        return {}
