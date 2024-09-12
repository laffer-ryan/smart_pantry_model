#!/bin/bash


# Load the .env file
source "$(dirname "$0")/.env"

# Check if the required environment variables are set
if [ -z "$KEY_PATH" ] || [ -z "$SOURCE_DIR" ] || [ -z "$ZIP_FILE_NAME" ] ||[ -z "$SOURCE_DIR2" ]||[ -z "$SOURCE_DIR3" ]||[ -z "$SOURCE_DIR4" ]|| [ -z "$DESTINATION_USER" ] || [ -z "$DESTINATION_HOST" ] || [ -z "$DESTINATION_PATH" ]; then
  echo "Missing required environment variables. Please check your .env file."
  exit 1
fi

# Zip the source directory or file
zip -r "$ZIP_FILE_NAME" "$SOURCE_DIR" "$SOURCE_DIR2" "$SOURCE_DIR3" "$SOURCE_DIR4" 

# Check if the zip command was successful
if [ $? -eq 0 ]; then
  echo "Zipped $SOURCE_DIR1 , $SOURCE_DIR2 , $SOURCE_DIR3 and $SOURCE_DIR4 to $ZIP_FILE_NAME successfully."
else
  echo "Failed to create zip file."
  exit 1
fi

# Use scp to copy the zip file to the remote server
scp -i "$PEM_FILE_PATH" "$ZIP_FILE_NAME" "$DESTINATION_USER@$DESTINATION_HOST:$DESTINATION_PATH"

# Check if the scp command was successful
if [ $? -eq 0 ]; then
  echo "File sent successfully."
  
  # Optionally, clean up the local zip file after transfer
  rm "$ZIP_FILE_NAME"
else
  echo "Failed to send file."
fi
