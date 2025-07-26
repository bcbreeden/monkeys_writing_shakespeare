import re
import string
import random
import time
from multiprocessing import Process, Manager

REMOVE_FORMATTING = True
REMOVE_PUNCTUATION = True
REMOVE_SPACES = True
REMOVE_CAPITALIZATION = True
NUMBER_OF_MONKEYS = 4


def read_text_file(file_name):
    """
    Read the contents of a text file.

    Args:
        file_name (str): The name of the text file to read, without the '.txt' extension.

    Returns:
        str: The full contents of the file as a string.
    """
    with open(f"{file_name}.txt", "r", encoding="utf-8") as file:
        text = file.read()
    return text


def format_text(text):
    """
    Format and clean text based on global configuration flags.

    Processing steps (if enabled by global flags):
        - REMOVE_FORMATTING: Collapses all whitespace (newlines, tabs, multiple spaces)
          into single spaces and strips leading/trailing spaces.
        - REMOVE_PUNCTUATION: Removes all punctuation characters.
        - REMOVE_SPACES: Removes all space characters.
        - REMOVE_CAPITALIZATION: Converts text to lowercase.

    Args:
        text (str): The raw text to be cleaned.

    Returns:
        str: The formatted and cleaned text.
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
    Build the alphabet used by the simulated monkeys based on global flags.

    Alphabet composition:
        - Always includes lowercase letters (a–z).
        - Includes uppercase letters if REMOVE_CAPITALIZATION is False.
        - Includes punctuation if REMOVE_PUNCTUATION is False.
        - Includes spaces if REMOVE_SPACES is False.
        - Includes newline and tab characters if REMOVE_FORMATTING is False.

    Returns:
        str: A string of characters representing the active alphabet.
    """
    alphabet = string.ascii_lowercase
    if not REMOVE_CAPITALIZATION:
        alphabet += string.ascii_uppercase
    if not REMOVE_PUNCTUATION:
        alphabet += string.punctuation
    if not REMOVE_SPACES:
        alphabet += " "
    if not REMOVE_FORMATTING:
        alphabet += "\n\t"
    return alphabet



def run_typewriter(text, monkey_id, winner_flag):
    """
    Each monkey types randomly until:
        - It finishes the text (and becomes the winner)
        - Or another monkey has already finished (winner_flag set)

    Args:
        text (str): Cleaned text to type.
        monkey_id (int): Monkey's unique identifier.
        winner_flag (Namespace): Shared flag to signal a winner.
    """
    alphabet = get_alphabet()
    attempt_index = 0
    key_presses = 0
    attempt_string = ""
    best_attempt = ""
    best_attempt_presses = 0

    while attempt_index < len(text):
        # Check if someone else already won
        if winner_flag.winner is not None:
            print(f"[Monkey {monkey_id}] stops, Monkey {winner_flag.winner} already won!")
            return

        key_presses += 1
        char = random.choice(alphabet)

        if char == text[attempt_index]:
            attempt_string += char
            attempt_index += 1
        else:
            if len(attempt_string) > len(best_attempt):
                best_attempt = attempt_string
                best_attempt_presses = key_presses
                print(f"[Monkey {monkey_id}] New best attempt "
                      f"({len(best_attempt)}/{len(text)}): "
                      f"'{best_attempt}' at trial #{best_attempt_presses}")
            attempt_index = 0
            attempt_string = ""

    # If we get here, this monkey finished first
    winner_flag.winner = monkey_id
    print(f"\n[Monkey {monkey_id}] 🎉 WINS after {key_presses} key presses! 🎉")
    print(f"[Monkey {monkey_id}] Final match: {attempt_string}")
    print(f"[Monkey {monkey_id}] Best attempt before win: "
          f"'{best_attempt}' (achieved at trial #{best_attempt_presses})")


def run_multiple_monkeys(text, number_of_monkeys):
    """
    Launch multiple simulated monkeys typing in parallel to match the given text.

    Each monkey runs in its own process and attempts to randomly generate characters
    to match the target text. The first monkey to complete the entire text is declared
    the winner, and all remaining monkeys stop typing immediately.

    Args:
        text (str): The target text for the monkeys to type. It should be pre-processed
            (e.g., using `format_text`) to match the intended alphabet configuration.
        number_of_monkeys (int): The number of monkey processes to spawn.

    Behavior:
        - Spawns `number_of_monkeys` processes, each running `run_typewriter()`.
        - Uses a shared flag (`winner_flag`) to signal when a monkey finishes.
        - Stops all other monkeys as soon as one completes the task.
        - Prints progress updates and declares the winning monkey.

    Returns:
        None
    """
    with Manager() as manager:
        winner_flag = manager.Namespace()
        winner_flag.winner = None

        processes = []
        for i in range(1, number_of_monkeys + 1):
            p = Process(target=run_typewriter, args=(text, i, winner_flag))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print(f"\nThe winner is Monkey {winner_flag.winner}! 🏆")


if __name__ == "__main__":
    text_to_type = read_text_file('shakespeare')
    clean_text = format_text(text_to_type)
    run_multiple_monkeys(clean_text, NUMBER_OF_MONKEYS)
