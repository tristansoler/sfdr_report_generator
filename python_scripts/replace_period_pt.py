import os
import re


def convert_decimal_format(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Normalize non-breaking spaces
    content = content.replace("\xa0", " ")

    # Updated regex to match:
    # - Percentages (e.g., 14.12%</span>%)
    # - "toneladas" (e.g., 687.4 toneladas)
    # - "GWh" (e.g., 0.3 GWh)
    pattern_general = r"(\d+)\.(\d+)(</[^>]+>)?\s?(%|\btoneladas\b|\bGWh\b)"

    # Specific pattern for exactly "0.0"
    pattern_zero = r"\b0\.0\b"

    # Pattern to remove space before "%"
    pattern_space_percent = r"(\d+)\s+%"

    # Pattern to remove space between "</span>" and "%"
    pattern_span_percent = r"(</span>)\s+%"

    # Replace decimal points with commas
    updated_content = re.sub(pattern_general, r"\1,\2\3 \4", content)
    updated_content = re.sub(pattern_zero, "0,0", updated_content)

    # Remove space before "%"
    updated_content = re.sub(pattern_space_percent, r"\1%", updated_content)

    # Remove space between "</span>" and "%"
    updated_content = re.sub(pattern_span_percent, r"\1%", updated_content)

    # change sociall for social
    updated_content = updated_content.replace("sociall", "social")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)


def process_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".html") and "_pt" in file_name:
                file_path = os.path.join(root, file_name)
                print(f"Processing: {file_path}")
                convert_decimal_format(file_path)


# Your directory
directory_path = r"C:\Users\n740789\Documents\sfdr_report_generator\final_reports"

process_files_in_directory(directory_path)
