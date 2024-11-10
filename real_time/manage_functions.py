import importlib
import inspect
import sys
from llm.generate_function import generate_function
import re

def add_function_for_level(level):
    """Requests a new function from GPT for a specific game level and appends it to dynamic.py."""
    print(f"Requesting new function for Level {level}...")
    
    response = generate_function()

    # 3. Clean and format the response to extract function code
    function_code = response

    # 4. Append the function code to dynamic.py
    try:
        with open("./real_time/dynamic.py", "a") as file:
            file.write("\n\n")  # Add spacing between functions for readability
            file.write(function_code)
        print(f"New function added for Level {level}.")
    except Exception as e:
        print(f"Error adding function for Level {level}: {e}")

    # 5. Extract the summary for displaying in the game
    summary = extract_summary(response)
    return summary

def load_and_execute_functions(module_name="real_time.dynamic"):
    """
    Loads all functions from a specified file and returns them for execution in the game.
    Maintains the order in which functions are defined in the file.
    """
    # Ensure the module is reloaded each time by removing it from sys.modules
    if module_name in sys.modules:
        del sys.modules[module_name]

    # Step 1: Extract function names from the file to preserve order
    function_order = []
    try:
        with open("./real_time/dynamic.py", "r") as file:
            lines = file.readlines()
            function_pattern = re.compile(r"^def\s+(\w+)\s*\(")
            for line in lines:
                match = function_pattern.match(line)
                if match:
                    function_order.append(match.group(1))

        # Step 2: Dynamically import the module and get all functions
        module = importlib.import_module(module_name)
        functions = {name: func for name, func in inspect.getmembers(module, inspect.isfunction)}

        # Step 3: Reorder functions based on their appearance in the file
        ordered_functions = {name: functions[name] for name in function_order if name in functions}

        # Step 4: Retrieve the last function in order
        if ordered_functions:
            last_function_name = list(ordered_functions.keys())[-1]
            last_function = ordered_functions[last_function_name]
            print(f"Function Loaded just: {last_function_name}")
            return {last_function_name: last_function}
        return ordered_functions

    except Exception as e:
        print(f"Error loading functions from dynamic.py: {e}")
        return {}

    
def reset_functions():
    with open("./dynamic.py", 'w') as file:
        file.write("""import pygame 
                   from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, clock
                    """)

def prepare_next_level(level):
    """Sets up and loads the new function for the next game level, including the summary."""
    # Step 1: Request and add a new function for the level
    summary = add_function_for_level(level)

    print("summary: " + summary)
    
    # Step 2: Load the functions from dynamic.py, including the newly added one
    functions = load_and_execute_functions()
    func_name, func = list(functions.items())[-1]



    # Step 3: Return both the functions and the summary text for display
    return func, summary

def extract_summary(response_text):
    """
    Extracts the summary section from the response text to display in the game.
    """
    summary_marker = "# Summary:"
    summary_text = ""
    in_summary_section = False
    
    for line in response_text.splitlines():
        if summary_marker in line:
            # Start capturing summary after marker
            summary_text += line.replace(summary_marker, "").strip()
            in_summary_section = True
        elif in_summary_section:
            # Continue adding summary lines until a blank line or function definition
            if line.strip() == "" or line.startswith("def "):
                break
            summary_text += " " + line.strip()
    
    return summary_text.strip()
