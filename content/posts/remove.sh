#!/bin/bash

# Loop through all subdirectories and process index.md files
for dir in */; do
  # Construct the path to the index.md file
  file="$dir/index.md"

  # Check if the index.md file exists
  if [[ -f "$file" ]]; then
    # Use sed to remove /images/ from the file
    sed -i "s|/images/||g" "$file"
    echo "Processed $file"
  fi
done