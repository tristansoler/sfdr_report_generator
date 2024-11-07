# %%
import re


def extract_placeholders(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Regular expression to match placeholders like {{PLACEHOLDER}}
    placeholders = re.findall(r"(\{\{.*?\}\})", content)

    # Remove duplicates by converting to a set, then back to a list
    placeholders = list(set(placeholders))

    return placeholders


# Example usage
file_path = r"C:\Users\n740789\Documents\sfdr_report_generator\narrative_templates\art8_spshares_10_narrative_template.html"
placeholders = extract_placeholders(file_path)
print("Placeholders found:")

# %%
for p in sorted(placeholders):
    print(p)

# %%
