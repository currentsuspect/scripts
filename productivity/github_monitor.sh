#!/bin/bash

# Load environment variables
if [ -f ~/scripts/.env ]; then
  source ~/scripts/.env
else
  echo "Error: .env file not found"
  exit 1
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

