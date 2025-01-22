import os
import re


def convert_decimal_format(file_path):
    # Read the content of the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Updated regex pattern to match cases like "47.30%" and "14.12</span>%"
    pattern = r"(\d+)\.(\d+)(</[^>]+>)?%"  # Optional HTML tag included

    # Replace the dot with a comma in matched patterns
    updated_content = re.sub(pattern, r"\1,\2\3%", content)

    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)


def process_files_in_directory(directory):
    # Iterate through all files in the given directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            # Check if the file is an HTML file and contains "_pt" in its name
            if file_name.endswith(".html") and "_pt" in file_name:
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")
                convert_decimal_format(file_path)


# Directory to process
directory_path = r"C:\Users\n740789\Documents\sfdr_report_generator\final_reports"

# Process files in the directory
process_files_in_directory(directory_path)
