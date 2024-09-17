import subprocess
import pyperclip

def get_last_command():
    # Fetch the last command from zsh history
    result = subprocess.run("fc -ln -1", shell=True, text=True, capture_output=True)
    return result.stdout.strip()

def get_last_output():
    # Fetch the output from the temporary log file
    temp_file = "/tmp/last_output.txt"
    try:
        with open(temp_file, "r") as file:
            output = file.read().strip()
        return output
    except FileNotFoundError:
        return ""

def main():
    print("What do you want to copy?")
    print("1: Last Command")
    print("2: Last Command Output")
    
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        last_command = get_last_command()
        pyperclip.copy(last_command)
        print(f"Copied to clipboard: {last_command}")

    elif choice == '2':
        last_output = get_last_output()
        if last_output:
            pyperclip.copy(last_output)
            print(f"Copied output to clipboard: {last_output}")
        else:
            print("No output found for the last command.")

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

