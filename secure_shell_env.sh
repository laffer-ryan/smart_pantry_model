#!/bin/bash

# Load the .env file
source "$(dirname "$0")/.env"

# Check if the required environment variables are set
if [ -z "$KEY_PATH" ] || [ -z "$DESTINATION_USER" ] || [ -z "$DESTINATION_HOST" ]; then
  echo "Missing required environment variables. Please check your .env file."
  exit 1
fi

# Ensure the SSH key has the correct permissions
chmod 600 "$KEY_PATH"

echo "SSH key permissions set to 600."

# Print the SSH command for easy access
echo "To SSH into the server, run:"
echo "ssh -i \"$KEY_PATH\" $DESTINATION_USER@$DESTINATION_HOST"
