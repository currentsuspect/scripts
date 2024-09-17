import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import json
import os
import time

# Define dictionary sources with URLs and HTML parsing details
dictionary_sources = {
    'merriam-webster': {
        'url': 'https://www.merriam-webster.com/dictionary/',
        'definition_selector': 'div.vg',
        'definition_class': 'span.dtText',
        'example_selector': 'span.exs',
    },
    'urban': {
        'url': 'https://www.urbandictionary.com/define.php?term=',
        'definition_selector': 'div.definition',
        'definition_class': 'div.meaning',
        'example_selector': 'div.example',
    },
}

# Cache file path
cache_file = 'definition_cache.json'

# Load cached definitions
def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}

# Save definitions to cache
def save_cache(cache):
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=4)

# Function to fetch and parse the dictionary page
def fetch_definition(word, source):
    url = f"{dictionary_sources[source]['url']}{word}"
    definition_selector = dictionary_sources[source]['definition_selector']
    definition_class = dictionary_sources[source]['definition_class']
    example_selector = dictionary_sources[source]['example_selector']
    
    retries = 3
    while retries > 0:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the definition section
            definition_section = soup.select_one(definition_selector)
            if not definition_section:
                return None

            # Extract the definition text
            definitions = definition_section.select(definition_class)
            if not definitions:
                return None

            # Clean up and return definitions
            cleaned_definitions = [definition.get_text(strip=True).replace(':', '').strip() for definition in definitions]

            # Extract usage examples if available
            examples = soup.select(example_selector)
            cleaned_examples = [example.get_text(strip=True).replace('\n', ' ').strip() for example in examples] if examples else None

            return cleaned_definitions, cleaned_examples

        except RequestException as e:
            print(f"Error fetching definition for '{word}' using {source}: {e}")
            retries -= 1
            time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred for '{word}' using {source}: {e}")
            return None

    return None

# Main function to handle user input and run the scraper
def main():
    # Load cache
    cache = load_cache()

    # Prompt the user for a word
    word = input("Enter a word to get its definition: ").strip()
    if not word:
        print("No word provided.")
        return

    # Prompt for source selection
    print("Available sources:")
    for idx, source in enumerate(dictionary_sources.keys(), start=1):
        print(f"{idx}. {source.capitalize()}")
    
    source_choice = int(input("Select a source by number: ")) - 1
    source_name = list(dictionary_sources.keys())[source_choice]

    # Check cache first
    if word in cache:
        print(f"Cached definition for '{word}' found.")
        use_cache = input("Do you want to use the cached result? (yes/no): ").strip().lower()
        if use_cache == 'yes':
            definitions = cache[word].get(source_name, {})
            if definitions:
                print(f"\nSource: {source_name.capitalize()}")
                if 'definitions' in definitions:
                    print(f"Definitions: {', '.join(definitions['definitions'])}")
                if 'examples' in definitions:
                    print(f"Usage Examples: {', '.join(definitions['examples'])}")
            else:
                print("No cached results available.")
            return

    # Fetch and print the definition from the selected source
    print(f"Fetching definitions for '{word}' from {source_name.capitalize()}:")
    result = fetch_definition(word, source_name)
    if result:
        definitions, examples = result
        all_definitions = {source_name: {
            'definitions': definitions,
            'examples': examples
        }}
        
        print(f"\nSource: {source_name.capitalize()}")
        if definitions:
            print(f"Definitions: {', '.join(definitions)}")
        if examples:
            print(f"Usage Examples: {', '.join(examples)}")
        
        # Save to cache
        cache.setdefault(word, {}).update(all_definitions)
        save_cache(cache)
    else:
        print(f"Could not fetch definition for '{word}' from {source_name.capitalize()}.")

if __name__ == "__main__":
    main()

