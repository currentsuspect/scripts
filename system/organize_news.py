import json
import os

def read_news(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"Successfully read data from {file_path}")
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return None

def format_news(data):
    formatted_news = []
    for item in data.get('articles', []):
        title = item.get('title', 'No Title')
        description = item.get('description', 'No Description')
        url = item.get('url', 'No URL')
        formatted_news.append(f"Title: {title}\nDescription: {description}\nURL: {url}\n\n")
    return "\n".join(formatted_news)

def write_to_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"News organized and written to {file_path}")
    except IOError:
        print(f"Error: Could not write to file {file_path}")

if __name__ == "__main__":
    news_file = os.path.expanduser('~/news.json')  # Update this path to the actual location
    output_file = os.path.expanduser('~/organized_news.txt')  # Specify the output text file path

    print(f"Reading news from {news_file}")
    news_data = read_news(news_file)
    if news_data:
        print("Formatting news data")
        formatted_news = format_news(news_data)
        print("Writing formatted news to file")
        write_to_file(formatted_news, output_file)
    else:
        print("No news data to process")

