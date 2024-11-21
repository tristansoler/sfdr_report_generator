import json
import pandas as pd
import os


def json_to_excel(json_file):
    # Get the directory and filename without extension
    directory = os.path.dirname(json_file)
    filename = os.path.splitext(os.path.basename(json_file))[0]

    # Create the Excel file path
    excel_file = os.path.join(directory, f"{filename}.xlsx")

    # Read the JSON file with UTF-8 encoding
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert JSON data to a pandas DataFrame

    # Check if the data is a dictionary
    if isinstance(data, dict):
        # If it's a flat dictionary, convert it to a DataFrame
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        # If it's a list of dictionaries, convert it to a DataFrame
        df = pd.DataFrame(data)
    else:
        raise ValueError("Unexpected JSON structure")

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")

    print(f"JSON file has been successfully converted to Excel.")
    print(f"Excel file saved at: {excel_file}")


# Example usage
json_file = r"C:\Users\n740789\Documents\sfdr_report_generator\python_scripts\polish_narrative.json"

json_to_excel(json_file)
