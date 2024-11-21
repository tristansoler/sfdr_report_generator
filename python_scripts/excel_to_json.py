import pandas as pd
import json
import os


def excel_to_json(excel_file):
    # Get the directory and filename without extension
    directory = os.path.dirname(excel_file)
    filename = os.path.splitext(os.path.basename(excel_file))[0]

    # Create the JSON file path
    json_file = os.path.join(directory, f"{filename}.json")

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Convert the DataFrame to a JSON string with ensure_ascii=False to preserve Unicode characters
    json_data = df.to_json(orient="records", force_ascii=False)

    # Write the JSON data to a file with UTF-8 encoding
    with open(json_file, "w", encoding="utf-8") as f:
        # Parse and re-dump the JSON to get proper formatting
        parsed_data = json.loads(json_data)
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)

    print(f"Excel file has been successfully converted to JSON.")
    print(f"JSON file saved at: {json_file}")


# Use the provided Excel file path
excel_file = r"C:\Users\n740789\Documents\sfdr_report_generator\excel_books\book1.xlsx"

excel_to_json(excel_file)
