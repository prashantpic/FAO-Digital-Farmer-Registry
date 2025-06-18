#!/bin/bash

# Define color codes
COLOR_RESET='\033[0m'
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_BLUE='\033[0;34m' # For INFO, or use default

# Function to log informational messages
log_info() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $1"
}

# Function to log warning messages
log_warning() {
    echo -e "${COLOR_YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] [WARNING] $1${COLOR_RESET}"
}

# Function to log error messages and exit
log_error() {
    echo -e "${COLOR_RED}[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR] $1${COLOR_RESET}" >&2
    exit 1
}

# Function to log success messages
log_success() {
    echo -e "${COLOR_GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] [SUCCESS] $1${COLOR_RESET}"
}

# Function to ask for user confirmation
# Returns 0 if user confirms (yes), 1 otherwise (no/default)
confirm_action() {
    local prompt_message="$1"
    local response

    while true; do
        read -r -p "$(echo -e "${COLOR_YELLOW}${prompt_message} [y/N]: ${COLOR_RESET}")" response
        case "$response" in
            [yY][eE][sS]|[yY])
                return 0 # Confirmed
                ;;
            [nN][oO]|[nN]|"") # Handles No or Enter (default to No)
                return 1 # Not confirmed
                ;;
            *)
                echo "Invalid input. Please enter 'y' for yes or 'n' for no."
                ;;
        esac
    done
}

# Ensure script is executable: chmod +x utils.sh
# To be sourced by other scripts: . /path/to/utils.sh