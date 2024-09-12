#!/bin/bash

# Check for sudo privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# List of required packages
dependencies=("python3-tk" "gdebi-core" "apt-transport-https")

# Function to check if a package is installed
is_installed() {
  dpkg -l | grep -qw "$1"
}

# Install missing dependencies
echo "Checking for missing dependencies..."
for dep in "${dependencies[@]}"; do
  if is_installed "$dep"; then
    echo "$dep is already installed."
  else
    echo "$dep is missing. Installing..."
    apt update && apt install -y "$dep"
    if [ $? -ne 0 ]; then
      echo "Failed to install $dep. Exiting."
      exit 1
    fi
  fi
done

# Check for the Python script in the same directory
SCRIPT_NAME="pickpac.py"
if [ ! -f "$SCRIPT_NAME" ]; then
  echo "Error: $SCRIPT_NAME not found in the current directory. Please ensure the script is present."
  exit 1
fi

# Copy the Python script to /usr/local/bin and make it executable
echo "Setting up the script..."
cp "$SCRIPT_NAME" /usr/local/bin/pickpac
chmod +x /usr/local/bin/pickpac

echo "Setup complete. You can now run 'pickpac' from the terminal."
