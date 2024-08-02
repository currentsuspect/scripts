#!/bin/bash

# Documentation
# This script monitors GitHub repositories for new issues and pull requests.
# If the .env file is missing, the script will prompt the user for the necessary information
# and save it to a new .env file. Ensure the .env file is not committed to version control.

ENV_FILE=~/scripts/.env

# Function to prompt for user input and save to .env file
prompt_for_env_vars() {
  # Function to prompt user for input and validate it
  read_input() {
    local prompt_message=$1
    local var_name=$2
    local input

    while true; do
      read -p "$prompt_message" input
      if [ -z "$input" ]; then
        echo "Error: $var_name cannot be empty."
      else
        echo "$input"
        break
      fi
    done
  }

  GITHUB_USER=$(read_input "Enter your GitHub username: " "GitHub username")
  TOKEN=$(read_input "Enter your GitHub token: " "GitHub token")
  REPOS_INPUT=$(read_input "Enter your repositories (comma-separated): " "Repositories")

  REPOS=$(echo $REPOS_INPUT | tr ',' ' ')

  # Save to .env file
  {
    echo "GITHUB_USER=$GITHUB_USER"
    echo "TOKEN=$TOKEN"
    echo "REPOS=($REPOS)"
  } > $ENV_FILE

  # Set file permissions to prevent unauthorized access
  chmod 600 $ENV_FILE

  echo "Environment variables saved to $ENV_FILE with restricted permissions."
}

# Load environment variables
if [ -f $ENV_FILE ]; then
  source $ENV_FILE
else
  echo "Error: .env file not found. Prompting for required information..."
  prompt_for_env_vars
fi

# Configuration
NOTIFY_CMD="notify-send"  # Adjust this if you're using a different notification system
LOG_FILE="$HOME/github_monitor.log"

# Function to fetch and parse issues or pull requests
fetch_updates() {
  local repo=$1
  local type=$2  # 'issues' or 'pulls'
  
  curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$GITHUB_USER/$repo/$type" |
    jq -r '.[] | "\(.title) (\(.html_url))"'
}

# Function to check for updates and send notifications
check_updates() {
  local repo=$1

  echo "Checking updates for $repo..."
  local issues=$(fetch_updates "$repo" "issues")
  local pulls=$(fetch_updates "$repo" "pulls")

  if [ -n "$issues" ] || [ -n "$pulls" ]; then
    echo "New updates for $repo:"
    echo "$issues" >> "$LOG_FILE"
    echo "$pulls" >> "$LOG_FILE"

    echo "$issues" | $NOTIFY_CMD -t 10000 -u normal -a "GitHub Monitor" -i info "New Issues in $repo"
    echo "$pulls" | $NOTIFY_CMD -t 10000 -u normal -a "GitHub Monitor" -i info "New Pull Requests in $repo"
  else
    echo "No new updates for $repo."
  fi
}

# Main loop
for repo in "${REPOS[@]}"; do
  check_updates "$repo"
done

