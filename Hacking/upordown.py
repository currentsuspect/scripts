import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

# Function to check the status of a URL
def check_status(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the status code indicates the site is up (200 OK)
        if response.status_code == 200:
            return (url, 'UP')
        else:
            return (url, 'DOWN')
    except RequestException as e:
        # Return the URL and the exception as 'DOWN'
        return (url, 'DOWN')

def main():
    # Ask user for the URLs
    url_input = input("Enter a list of URLs separated by commas: ")
    urls = [url.strip() for url in url_input.split(',')]

    # Number of threads to use for parallel requests
    num_threads = 5

    # Set up the ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to check the status of each URL
        futures = [executor.submit(check_status, url) for url in urls]

        # Process results as they are completed
        for future in as_completed(futures):
            url, status = future.result()
            print(f'URL: {url}, Status: {status}')

# Run the script
if __name__ == "__main__":
    main()

