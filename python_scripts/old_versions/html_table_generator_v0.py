import pandas as pd
from bs4 import BeautifulSoup

# add feature to translate values column "Sector"

# Read the Excel file
df = pd.read_excel(
    r"C:\Users\n740789\Documents\sfdr_report_generator\excel_books\test_fund_content.xlsx"
)

# Generate the HTML table
html_str = df.to_html(classes="dataframe", index=False)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_str, "html.parser")


# Function to safely remove an element if it exists
def safe_remove(element):
    if element:
        element.decompose()


# Remove the first th from the header if it exists (in case of an index)
header_row = soup.find("thead").find("tr")
safe_remove(header_row.find("th"))

# Remove the first td from each row in the body if it exists (in case of an index)
for row in soup.find("tbody").find_all("tr"):
    safe_remove(row.find("td"))

# Extract the modified table body content
table_body = soup.find("tbody")

# Get the actual column names from the DataFrame
column_names = df.columns.tolist()

# Create the new table structure
new_table = f"""
<div class="table-body" id="q03_t1">
    <table class="dataframe">
        <colgroup>
            <col class="col1">
            <col class="col2">
            <col class="col3">
            <col class="col4">
        </colgroup>
        <thead>
            <tr>
                {"".join(f"<th>{col}</th>" for col in column_names)}
            </tr>
        </thead>
        {str(table_body)}
    </table>
</div>
"""

# Print or save the new table
print(new_table)

# Optionally, save to a file
# with open('robust_table.html', 'w', encoding='utf-8') as f:
#     f.write(new_table)
