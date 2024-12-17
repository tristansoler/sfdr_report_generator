import pandas as pd
from bs4 import BeautifulSoup


def extract_content(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    data = {}
    for element in soup.find_all(id=True):
        id = element["id"]
        content = element.decode_contents().strip()
        data[id] = content

    return data


def create_excel(data, output_file):
    df = pd.DataFrame.from_dict(data, orient="index").transpose()
    df.to_excel(output_file, index=False)
    print(f"Excel file created: {output_file}")


if __name__ == "__main__":
    html_file = "template.html"  # Replace with your HTML file name
    output_file = "template_ids_content.xlsx"

    data = extract_content(html_file)
    create_excel(data, output_file)
