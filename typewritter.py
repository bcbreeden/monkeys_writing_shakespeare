import re
import string
import random
import time

REMOVE_FORMATTING = True
REMOVE_PUNCTUATION = True
REMOVE_SPACES = True
REMOVE_CAPITALIZATION = True

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
        - REMOVE_CAPITALIZATION: Converts text to lowercase if True.

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
    if REMOVE_CAPITALIZATION:
        text = text.lower()
    return text


def get_alphabet():
    """
    Build the alphabet dynamically based on global formatting flags.

    Returns:
        str: A string of characters allowed for random generation.
    """
    # Start with lowercase always
    alphabet = string.ascii_lowercase

    # Add uppercase letters only if capitalization is kept
    if not REMOVE_CAPITALIZATION:
        alphabet += string.ascii_uppercase

    # Add punctuation if allowed
    if not REMOVE_PUNCTUATION:
        alphabet += string.punctuation

    # Add spaces if allowed
    if not REMOVE_SPACES:
        alphabet += " "

    # Add newlines/tabs if formatting is preserved
    if not REMOVE_FORMATTING:
        alphabet += "\n\t"

    return alphabet


def run_typewriter(text):
    """
    Simulate a typewriter randomly pressing keys until the target text is matched.

    The alphabet is dynamically determined based on global flags:
        - REMOVE_FORMATTING controls inclusion of newlines/tabs.
        - REMOVE_PUNCTUATION controls punctuation.
        - REMOVE_SPACES controls spaces.
        - REMOVE_CAPITALIZATION controls inclusion of uppercase letters.

    Args:
        text (str): The target text to match. 
                    It should already be cleaned using `format_text()`.

    Returns:
        int: The total number of key presses required to produce the target text.
    """
    alphabet = get_alphabet()
    attempt_index = 0
    key_presses = 0
    attempt_string = ""
    best_attempt = ""
    best_attempt_presses = 0

    while attempt_index < len(text):
        key_presses += 1
        char = random.choice(alphabet)

        # Check if character matches the target at current index
        if char == text[attempt_index]:
            attempt_string += char
            attempt_index += 1
        else:
            # If this was the best attempt so far, store it and print info
            if len(attempt_string) > len(best_attempt):
                best_attempt = attempt_string
                best_attempt_presses = key_presses
                print(f"New best attempt ({len(best_attempt)}/{len(text)}): "
                      f"'{best_attempt}' at trial #{best_attempt_presses}")
            # Reset on mismatch
            attempt_index = 0
            attempt_string = ""

    print(f"\nFinal match: {attempt_string}")
    print(f"Best attempt before final match: '{best_attempt}' "
          f"(achieved at trial #{best_attempt_presses})")
    return key_presses


if __name__ == "__main__":
    text_to_type = read_text_file('shakespeare')
    clean_text = format_text(text_to_type)
    run_typewriter(clean_text)