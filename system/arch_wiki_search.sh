#!/bin/bash

# Configuration
WIKI_API_URL="https://en.wikipedia.org/w/api.php"
SEARCH_QUERY="Arch Linux"
SEARCH_LANG="en"

# Check for required commands
command -v curl >/dev/null 2>&1 || { echo "Error: curl is not installed."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "Error: jq is not installed."; exit 1; }

# Function to fetch and display the top search result
search_arch_wiki() {
    local query=$1
    local lang=$2

    # URL encode the query
    local encoded_query
    encoded_query=$(echo "$query" | jq -sRr @uri)

    # Fetch search results from the Arch Wiki API
    local response
    response=$(curl -s "$WIKI_API_URL?action=query&format=json&list=search&srsearch=$encoded_query&utf8=1")

    # Parse the response and extract the title and URL of the top search result
    local title
    title=$(echo "$response" | jq -r '.query.search[0].title')
    
    if [ "$title" == "null" ]; then
        echo "No results found for '$query'."
        exit 1
    fi

    local url
    url="https://wiki.archlinux.org/title/${title// /_}"

    # Display the result
    echo "Top search result for '$query':"
    echo "Title: $title"
    echo "URL: $url"
}

# Check for user input
if [ $# -eq 0 ]; then
    echo "Usage: $0 <search_term>"
    exit 1
fi

# Perform the search
search_arch_wiki "$1" "$SEARCH_LANG"

