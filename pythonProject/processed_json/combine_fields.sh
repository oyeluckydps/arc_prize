#!/bin/bash

# Set the directory containing the text files
DIRECTORY="./evaluation_challenges/"
# Set the output file path
OUTPUT_FILE="./evaluation_challenges/combined.txt"

# Empty the output file if it already exists
> "$OUTPUT_FILE"

# Loop through each text file in the directory
for FILE in "$DIRECTORY"/*.json
do
    # Get the filename without the path and extension
    FILENAME=$(basename "$FILE" .json)
    # Add the filename as a heading
    echo "## $FILENAME" >> "$OUTPUT_FILE"
    # Add the file content
    cat "$FILE" >> "$OUTPUT_FILE"
    # Add an empty line for separation
    echo "" >> "$OUTPUT_FILE"
done

echo "Files combined successfully into $OUTPUT_FILE"

