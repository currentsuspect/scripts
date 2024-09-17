# utils.py

def print_message(message):
    """Print a message to the user."""
    print("\n" + message + "\n")

def get_choice(choices):
    """Prompt the user for a choice and validate the input."""
    while True:
        choice = input("Your choice: ").strip().lower()
        if choice in choices:
            return choice
        else:
            print("Invalid choice. Please try again.")

