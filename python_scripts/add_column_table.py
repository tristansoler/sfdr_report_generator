import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def process_html_file(html_file_path, mapping_excel_path):
    """
    Process an HTML file by finding the <div id="q04_t">, modifying its table,
    and returning the modified HTML as a string.

    Transformation steps:
      1. Convert the table to a pandas DataFrame.
      2. Rename the column 'Sectors' (or 'Sector') to 'Subsector'.
      3. Merge with the mapping Excel file to add a 'Sectors' column.
      4. Reorder columns to: Sectors, Subsector, % Assets.
      5. Convert back to an HTML table with a <colgroup> containing three <col> tags.
    """
    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Locate the <div> with id="q04_t"
    div_q04_t = soup.find("div", id="q04_t")
    if not div_q04_t:
        raise ValueError("Div with id 'q04_t' not found in the HTML file.")

    # Find the table within the div
    table_tag = div_q04_t.find("table")
    if not table_tag:
        raise ValueError("No table found inside the div with id 'q04_t'.")

    # Convert the table HTML to a DataFrame (using StringIO to avoid warnings)
    table_html = str(table_tag)
    dfs = pd.read_html(StringIO(table_html))
    if not dfs:
        raise ValueError("No table could be parsed from the HTML snippet.")
    df = dfs[0]

    # Rename the column "Sectors" (or "Sector") to "Subsector"
    if "Sectors" in df.columns:
        df.rename(columns={"Sectors": "Subsector"}, inplace=True)
    elif "Sector" in df.columns:
        df.rename(columns={"Sector": "Subsector"}, inplace=True)
    else:
        raise ValueError(
            "Expected column 'Sectors' or 'Sector' not found in the table."
        )

    # Read the mapping Excel file into a DataFrame
    map_sector_df = pd.read_excel(mapping_excel_path)
    if (
        "Subsectors" not in map_sector_df.columns
        or "Sectors" not in map_sector_df.columns
    ):
        raise ValueError(
            "Mapping Excel file must contain 'Subsectors' and 'Sectors' columns."
        )

    # Merge the original DataFrame with the mapping DataFrame.
    merged_df = pd.merge(
        df, map_sector_df, left_on="Subsector", right_on="Subsectors", how="left"
    )
    merged_df.drop(columns=["Subsectors"], inplace=True)
    merged_df = merged_df[["Sectors", "Subsector", "% Assets"]]

    # rename columns "Subsector" to "Subsectors"
    merged_df.rename(columns={"Subsector": "Subsectors"}, inplace=True)

    # Convert the merged DataFrame back into an HTML table.
    new_table_html = merged_df.to_html(index=False, border=0, classes="table")

    # Modify the table HTML to include a colgroup with three <col> elements.
    new_table_soup = BeautifulSoup(new_table_html, "html.parser")
    new_table_tag = new_table_soup.find("table")
    colgroup_tag = new_table_soup.new_tag("colgroup")
    for col_class in ["col1", "col2", "col3"]:
        col_tag = new_table_soup.new_tag("col", **{"class": col_class})
        colgroup_tag.append(col_tag)
    new_table_tag.insert(0, colgroup_tag)

    # Replace the old table in the div with the new table.
    table_tag.replace_with(new_table_tag)

    # Return the modified HTML as a string.
    return str(soup)
