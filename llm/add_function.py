def append_to_python_file(content: str):
    try:
        with open("dynamic.py", "a") as file:
            file.write(content)
            file.close()
        print(f"Content successfully appended to {"dynamic.py"}")

    except Exception as e:
        print(f"An error occurred: {e}")