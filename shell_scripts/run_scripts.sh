#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Determine the correct Python command
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if target language parameter is given
if [ -n "$1" ]; then
    LANGUAGE=$1
    echo "Using provided language: $LANGUAGE"
else
    echo "No language provided. Scripts will prompt for input if needed."
fi

# Array of scripts to run
SCRIPTS=(
    "/c/Users/n740789/Documents/sfdr_report_generator/python_scripts/00_data_preper.py"
    "/c/Users/n740789/Documents/sfdr_report_generator/python_scripts/01_template_builder.py"
    "/c/Users/n740789/Documents/sfdr_report_generator/python_scripts/02_report_builder.py"
)

# Run Python scripts in sequence, passing the target language as a parameter if provided
for script in "${SCRIPTS[@]}"; do
    echo "Running $script"
    if [ -n "$LANGUAGE" ]; then
        $PYTHON_CMD "$script" "$LANGUAGE"
    else
        $PYTHON_CMD "$script"
    fi

    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error running $script"
        exit 1
    fi
done

echo "All scripts completed successfully."