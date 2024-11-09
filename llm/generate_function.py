from api_call import GPT

def generate_function(gpt: GPT):
    user_prompt = open(f"./prompts/user_prompt.txt", "r").read() + open(f"../real-time/dynamic.py", "r").read()
    system_prompt = open(f"./prompts/system_prompt.txt", "r").read()

    # generate response
    response = gpt.text_completion(user_prompt=user_prompt, system_prompt=system_prompt)

    # remove unecessary ```
    return remove_code_block_markers(response)

def remove_code_block_markers(text):  # Removes ```python and ``` markers from the given text
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if line.strip() != '```python' and line.strip() != '```']
    return '\n'.join(cleaned_lines)


# For testing purposes
def main():
    gpt = GPT()
    print(generate_function(gpt))
    pass

if __name__ == "__main__":
    main()
