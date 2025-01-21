import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_translations():
    """Load translations from JSON file"""
    script_dir = Path(__file__).resolve().parent
    translations_path = script_dir / "translations.json"

    print(f"Attempting to load translations from: {translations_path}")  # Debug print

    if not translations_path.exists():
        raise FileNotFoundError(f"Translations file not found at {translations_path}")

    with open(translations_path, "r", encoding="utf-8") as f:
        return json.load(f)


TRANSLATIONS = load_translations()


def translate_text(text, target_language):
    """
    Translate text using the predefined dictionary
    """
    if target_language == "en":
        return text
    return TRANSLATIONS.get(target_language, {}).get(text, text)


def generate_html_table(df, table_structure="investment", target_language=None):
    """
    Generate HTML table without the wrapper div and translate content

    Parameters:
    df : pandas DataFrame
        The data to convert to HTML
    table_structure : str
        Either 'investment' or 'sector' to determine the table structure
    target_language : str
        The target language code for translation
    """

    if target_language is None:
        target_language = main()

    # Format percentage values
    def process_percentage(value):
        if pd.isna(value):
            return np.nan
        try:
            return float(value.strip("%")) / 100
        except AttributeError:
            return value

    # Apply this function to your percentage columns
    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = df[col].apply(process_percentage)
        # Then, when formatting for display
        df[col] = df[col].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "")

    # Translate column names
    df.columns = [translate_text(col, target_language) for col in df.columns]

    # Translate content (except for all-uppercase columns)
    for col in df.columns:
        if col.upper() != col:  # Skip columns with all uppercase names
            df.loc[:, col] = df[col].apply(
                lambda x: (
                    translate_text(str(x), target_language) if pd.notnull(x) else x
                )
            )

    # Generate the initial HTML table
    html_str = df.to_html(classes="dataframe", index=False, escape=False)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_str, "html.parser")

    # Define column structure based on table type
    if table_structure == "investment":
        colgroup = """
            <colgroup>
                <col class="col1">
                <col class="col2">
                <col class="col3">
                <col class="col4">
            </colgroup>
        """
    else:  # sector structure
        colgroup = """
            <colgroup>
                <col class="col1">
                <col class="col2">
            </colgroup>
        """

    # Create the table structure without the wrapper div
    new_table = f"""
        <table>
            {colgroup}
            <thead>
                <tr>
                    {"".join(f"<th>{col}</th>" for col in df.columns)}
                </tr>
            </thead>
            {str(soup.find("tbody"))}
        </table>
    """

    return new_table


def main(language=None):
    if language is None:
        if len(sys.argv) > 1:
            language = sys.argv[1]
        else:
            try:
                language = input("Enter the language code (es, en, pt, or pl): ")
            except ValueError as e:
                print(e)
                logging.error(e)

    if not isinstance(language, str) or language not in ["es", "en", "pt", "pl"]:
        raise ValueError(
            "Invalid language code. Please enter 'es', 'en', 'pt', or 'pl'."
        )

    return language


if __name__ == "__main__":
    input_language = main()
