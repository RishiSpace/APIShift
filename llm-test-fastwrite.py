import os
from FastWrite import generate_documentation_gemini, generate_documentation_groq, generate_documentation_openai


def read_python_file(file_path):
    """
    Reads a Python (.py) file and returns its content as a string.
    
    :param file_path: Path to the Python file.
    :return: String containing the file's content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Example usage
code_content = read_python_file("APIShift/conversation.py")
print(code_content)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

custom_prompt = """
Objective:
Generate detailed documentation for Python code. Include inline comments, function descriptions, module overviews, and best practices.
"""


output_gemini = generate_documentation_gemini(code_content, custom_prompt)
output_groq = generate_documentation_groq(code_content, custom_prompt)
output_openai = generate_documentation_openai(code_content, custom_prompt)

print (f"Gemini:\n\n\n{output_gemini}\n\n Groq:\n\n\n{output_groq}\n\n OpenAI:\n\n\n{output_openai}")