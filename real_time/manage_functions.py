import importlib
import inspect
import sys
from llm.api_call import GPT

def add_function_for_level(level):
    """Requests a new function from GPT for a specific game level and appends it to dynamic.py."""
    print(f"Requesting new function for Level {level}...")
    
    # 1. Construct the prompts based on the level and current game state
    user_prompt = open("./llm/prompts/user_prompt.txt", "r").read() + f"\nAdd a unique gameplay mechanic for Level {level}."
    system_prompt = open("./llm/prompts/system_prompt.txt", "r").read()

    # 2. Request the function from GPT
    gpt = GPT()
    response = gpt.text_completion(user_prompt=user_prompt, system_prompt=system_prompt)

    # 3. Clean and format the response to extract function code
    function_code = remove_code_block_markers(response)

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
    """
    # Ensure the module is reloaded each time by removing it from sys.modules
    if module_name in sys.modules:
        del sys.modules[module_name]

    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        # Get all functions defined in the module
        functions = {name: func for name, func in inspect.getmembers(module, inspect.isfunction)}
        print("Functions Loaded just now are: ", functions)
        return functions
    except Exception as e:
        print(f"Error loading functions from {module_name}: {e}")
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

    # Step 2: Load the functions from dynamic.py, including the newly added one
    functions = load_and_execute_functions()

    # Step 3: Return both the functions and the summary text for display
    return functions, summary

def remove_code_block_markers(text):
    """Removes ```python and ``` markers from the given text."""
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if line.strip() != '```python' and line.strip() != '```']
    return '\n'.join(cleaned_lines)

def extract_summary(response_text):
    """Extracts the summary section from the GPT response to display in the game."""
    summary_marker = "# Summary:"
    summary_text = ""
    for line in response_text.splitlines():
        if summary_marker in line:
            summary_text += line.replace(summary_marker, "").strip()
        elif summary_text:
            # Continue adding summary lines until a blank line or function definition
            if line.strip() == "" or line.startswith("def "):
                break
            summary_text += " " + line.strip()
    return summary_text.strip()
