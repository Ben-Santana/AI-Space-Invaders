import importlib
import inspect
import sys
from llm.api_call import GPT


def remove_code_block_markers(text):
    """Removes ```python and ``` markers from the given text."""
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if line.strip() != '```python' and line.strip() != '```']
    return '\n'.join(cleaned_lines)


def extract_summary(response):
    """Extracts the summary from the response if available."""
    summary_marker = "# Summary:"
    if summary_marker in response:
        return response.split(summary_marker, 1)[1].strip()
    return "No summary provided."


def add_function_for_level(level):
    """Requests a new function from GPT for a specific game level and appends it to real_time/dynamic.py."""
    print(f"Requesting new function for Level {level}...")

    # Construct the prompts based on the level and current game state
    user_prompt = open("./llm/prompts/user_prompt.txt", "r").read() + f"\nAdd a unique gameplay mechanic for Level {level}."
    system_prompt = open("./llm/prompts/system_prompt.txt", "r").read()

    # Request the function from GPT
    gpt = GPT()
    response = gpt.text_completion(user_prompt=user_prompt, system_prompt=system_prompt)

    # Clean and format the response to extract function code
    function_code = remove_code_block_markers(response)

    # Add necessary imports at the top of the generated code
    function_code = "import pygame\n" + function_code

    # Append the function code to real_time/dynamic.py
    try:
        with open("real_time/dynamic.py", "a") as file:
            file.write("\n\n")  # Add spacing between functions for readability
            file.write(function_code)
        print(f"New function added for Level {level}.")
    except Exception as e:
        print(f"Error adding function for Level {level}: {e}")

    # Extract the summary for displaying in the game
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


def prepare_next_level(level):
    """Generates a new function for the level and loads all functions for execution."""
    # Request a new function for the current level and append it to dynamic.py
    level_summary = add_function_for_level(level)
    
    # Load all functions from dynamic.py for execution
    dynamic_functions = load_and_execute_functions("real_time.dynamic")
    
    return dynamic_functions, level_summary
