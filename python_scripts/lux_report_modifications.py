import os
import glob
from add_column_table import process_html_file  # Import the transformation function

# Define the directory containing your final report HTML files
final_reports_dir = r"C:\Users\n740789\Documents\sfdr_report_generator\final_reports"

# Define the file pattern (raw string to avoid escaping backslashes)
file_pattern = r"20250227_*en.html"

# Build the full search pattern (e.g. "C:\...\final_reports\20250227_*en.html")
search_pattern = os.path.join(final_reports_dir, file_pattern)

# Define the mapping Excel file path (as used in add_column_table.py)
mapping_excel_path = r"C:\Users\n740789\Downloads\Sector-Subsector_Distribution.xlsx"

# Get a list of all matching files
html_files = glob.glob(search_pattern)

if not html_files:
    print("No HTML files matching the pattern were found.")
else:
    for file_path in html_files:
        print(f"Processing file: {file_path}")
        # Process the file using the function from add_column_table.py
        modified_html = process_html_file(file_path, mapping_excel_path)

        # Write the modified HTML back to the file (or to a new file if preferred)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_html)

        print(f"Saved modified file: {file_path}")

print("All files have been processed.")
