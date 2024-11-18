import pandas as pd
from bs4 import BeautifulSoup


def generate_html_table(df, table_structure="investment"):
    """
    Generate HTML table without the wrapper div

    Parameters:
    df : pandas DataFrame
        The data to convert to HTML
    table_structure : str
        Either 'investment' or 'sector' to determine the table structure
    """

    # Remove the first row
    df = df.iloc[1:]

    # Format percentage values
    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = df[col].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "")

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


# If running as main script, test the function
if __name__ == "__main__":
    # Test data
    test_df = pd.DataFrame(
        {"Column1": ["Test1", "Test2"], "Column2": ["Value1", "Value2"]}
    )

    print(generate_html_table(test_df, "sector"))
