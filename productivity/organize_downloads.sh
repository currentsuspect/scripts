#!/bin/bash

# Directories to move files to
IMAGE_DIR="$HOME/Pictures/Downloads"
DOCUMENT_DIR="$HOME/Documents/Downloads"
VIDEO_DIR="$HOME/Videos/Downloads"
AUDIO_DIR="$HOME/Music/Downloads"
OTHER_DIR="$HOME/Other/Downloads"
MISC_DIR="$HOME/Miscellaneous/Downloads"
DOWNLOADS_DIR="$HOME/Downloads"

# Create directories if they do not exist
mkdir -p "$IMAGE_DIR" "$DOCUMENT_DIR" "$VIDEO_DIR" "$AUDIO_DIR" "$OTHER_DIR" "$MISC_DIR"

# Error handling function
error_handling() {
  echo "Error: $1"
  exit 1
}

# Check for required commands
command -v mv >/dev/null 2>&1 || error_handling "mv command not found"
command -v mkdir >/dev/null 2>&1 || error_handling "mkdir command not found"
command -v find >/dev/null 2>&1 || error_handling "find command not found"
command -v rmdir >/dev/null 2>&1 || error_handling "rmdir command not found"

# Function to move files based on extension
move_files() {
  local dir=$1
  shift
  for ext in "$@"; do
    find "$DOWNLOADS_DIR" -type f -iname "*.$ext" -exec mv {} "$dir" \; 2>/dev/null
  done
}

# Check if Downloads directory exists
if [ -d "$DOWNLOADS_DIR" ]; then
  # Move files to respective directories
  move_files "$IMAGE_DIR" jpg jpeg png gif bmp
  move_files "$DOCUMENT_DIR" pdf doc docx xls xlsx ppt pptx txt
  move_files "$VIDEO_DIR" mp4 mkv avi mov
  move_files "$AUDIO_DIR" mp3 wav flac

  # Move remaining files to Other directory
  find "$DOWNLOADS_DIR" -type f -exec mv {} "$OTHER_DIR" \; 2>/dev/null

  # Move unknown files to Miscellaneous directory
  find "$DOWNLOADS_DIR" -type f -exec mv {} "$MISC_DIR" \; 2>/dev/null

  # Remove empty directories in Downloads
  find "$DOWNLOADS_DIR" -type d -empty -exec rmdir {} \; 2>/dev/null

  # Ensure log directory exists
  mkdir -p "$DOWNLOADS_DIR"

  # Log the action
  log_file="$DOWNLOADS_DIR/organize.log"
  {
    echo "Organized Downloads on $(date)"
    echo "Images moved to $IMAGE_DIR"
    echo "Documents moved to $DOCUMENT_DIR"
    echo "Videos moved to $VIDEO_DIR"
    echo "Audio files moved to $AUDIO_DIR"
    echo "Other files moved to $OTHER_DIR"
    echo "Unknown files moved to $MISC_DIR"
    echo "Empty directories removed"
  } >> "$log_file"

  echo "Downloads folder organized successfully."

else
  echo "Downloads directory does not exist. Skipping organization."
fi

