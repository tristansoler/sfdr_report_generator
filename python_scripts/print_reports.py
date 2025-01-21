import os
import sys
import logging
import pdfkit
from html_table_generator import main as get_language

# Path to wkhtmltopdf.exe (update this path)
wkhtmltopdf_path = r"C:\Users\n740789\Documents\wkhtmltox\bin\wkhtmltopdf.exe"

# Configure pdfkit to use this path
pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


def convert_html_to_pdf(date, language):
    base_dir = r"C:\Users\n740789\Documents\sfdr_report_generator\final_reports"
    output_dir = os.path.join(base_dir, "final_reports_pdf", date[:4], language)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Filter HTML files by date prefix
    html_files = [
        file
        for file in os.listdir(base_dir)
        if file.startswith(date) and file.endswith(".html")
    ]

    if not html_files:
        print(f"No HTML files found with the prefix '{date}' in {base_dir}.")
        return

    for html_file in html_files:
        input_path = os.path.join(base_dir, html_file)
        output_filename = os.path.splitext(html_file)[0] + ".pdf"
        output_path = os.path.join(output_dir, output_filename)

        try:
            # Convert HTML to PDF
            pdfkit.from_file(input_path, output_path)
            print(f"Converted: {html_file} -> {output_path}")
        except Exception as e:
            logging.error(f"Failed to convert {html_file} to PDF: {e}")


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py <YYYYMMDD> <language>")
        date = input("Enter the date (YYYYMMDD): ").strip()
        language = get_language()
    else:
        date = sys.argv[1].strip()
        language = sys.argv[2].strip().lower()

    # Validate date format
    if not date.isdigit() or len(date) != 8:
        print("Invalid date format. Please provide a date in 'YYYYMMDD' format.")
        sys.exit(1)

    # Validate language using the get_language function
    try:
        language = get_language(language)
    except ValueError as e:
        print(e)
        sys.exit(1)

    convert_html_to_pdf(date, language)
