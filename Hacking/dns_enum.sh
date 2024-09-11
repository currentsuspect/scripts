#!/bin/bash

# Usage: ./dns_enum.sh <domain> [options]
# Example: ./dns_enum.sh example.com --brute --passive --output /path/to/output.txt

# Default settings
OUTPUT_FILE="combined_output.txt"
BRUTE_FORCE=0
PASSIVE_MODE=0

# Path to the wordlist
WORDLIST_PATH="/path/to/SecLists/Discovery/DNS/subdomains-top1million-5000.txt"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if necessary tools are installed
if ! command_exists dnsenum; then
    echo "[ERROR] dnsenum is not installed. Please install it and try again."
    exit 1
fi

if ! command_exists amass; then
    echo "[ERROR] amass is not installed. Please install it and try again."
    exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_FILE="$2"
            shift # past argument
            shift # past value
            ;;
        --brute)
            BRUTE_FORCE=1
            shift # past argument
            ;;
        --passive)
            PASSIVE_MODE=1
            shift # past argument
            ;;
        *)
            DOMAIN="$1"
            shift # past domain
            ;;
    esac
done

# Check if domain is provided
if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain> [options]"
    echo "Options:"
    echo "  --output <file>  Specify output file (default: combined_output.txt)"
    echo "  --brute          Enable brute-force subdomain enumeration"
    echo "  --passive        Enable passive mode for amass"
    exit 1
fi

echo "[INFO] Starting DNS enumeration for domain: $DOMAIN"

# Log file to capture output
LOG_FILE="dns_enum_log.txt"
exec > >(tee -i $LOG_FILE) 2>&1

echo "[INFO] Running dnsenum..."
if ! dnsenum $DOMAIN > dnsenum_output.txt; then
    echo "[ERROR] dnsenum failed. Check log for details."
    exit 1
fi

echo "[INFO] Running amass..."
AMASS_OPTIONS=""
if [ $BRUTE_FORCE -eq 1 ]; then
    AMASS_OPTIONS="$AMASS_OPTIONS -brute -w $WORDLIST_PATH"
fi
if [ $PASSIVE_MODE -eq 1 ]; then
    AMASS_OPTIONS="$AMASS_OPTIONS -passive"
fi

if ! amass enum -d $DOMAIN $AMASS_OPTIONS -o amass_output.txt; then
    echo "[ERROR] amass failed. Check log for details."
    exit 1
fi

echo "[INFO] Combining results..."
cat dnsenum_output.txt amass_output.txt | sort | uniq > $OUTPUT_FILE

echo "[INFO] DNS enumeration complete. Results saved to $OUTPUT_FILE"
echo "[INFO] Log file saved to $LOG_FILE"

