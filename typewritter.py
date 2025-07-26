import re
import string

REMOVE_FORMATTING = True
REMOVE_PUNCTUATION = True
REMOVE_SPACES = True


def read_text_file(file_name):
    """
    Read the contents of a text file.

    Args:
        file_name (str): The name of the text file (without extension) to read.

    Returns:
        str: The entire contents of the file as a single string.
    """
    with open(f"{file_name}.txt", "r", encoding="utf-8") as file:
        text = file.read()
    return text


def format_text(text):
    """
    Format and clean a string based on global flags.

    Operations performed (depending on global flags):
        - REMOVE_FORMATTING: Collapses all whitespace (newlines, tabs, multiple spaces) into single spaces.
        - REMOVE_PUNCTUATION: Removes punctuation characters using string.punctuation.
        - REMOVE_SPACES: Removes all remaining spaces from the string.

    Args:
        text (str): The input string to format.

    Returns:
        str: The formatted and cleaned string.
    """
    if REMOVE_FORMATTING:
        text = re.sub(r'\s+', ' ', text).strip()
    if REMOVE_PUNCTUATION:
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
    if REMOVE_SPACES:
        text = text.replace(" ", "")
    return text


