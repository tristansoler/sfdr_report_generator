# SFDR Post-Contractual Report Generator

An internal tool for generating Sustainable Finance Disclosure Regulation (SFDR) post-contractual reports. This project is designed for use within our company's ESG Global division and its various geographical units.

## Project Overview

This tool automates the creation of standardized SFDR post-contractual reports, processing data from internal Excel sources and generating formatted HTML reports with visualizations.

## Project Structure

```
sfdr_report_generator/
├── python_scripts/           # Core Python processing scripts
│   ├── 00_data_preper.py     # Data preparation and processing
│   ├── 01_template_builder.py# HTML template generation
│   ├── 02_report_builder.py  # Final report assembly
│   ├── html_table_generator.py # Table formatting utilities
│   └── plot_builder.py       # Data visualization generation
├── excel_books/              # Input Excel data files
│   ├── aladdin_data/         # Source data files
│   └── *.xlsx                # Configuration and mapping files
├── narrative_templates/      # HTML templates for reports
├── final_processed_data/     # Processed data output
└── final_reports/            # Generated HTML reports
├── graphs_plots/         # Generated visualizations
└── logos_icons/          # Static assets
```

## Features

- Automated processing of internal Excel-based SFDR data
- Generation of post-contractual HTML reports
- Dynamic data visualization and charting
- Configurable templates and narratives
- Support for multiple fund types and reporting requirements

## Prerequisites

- Python 3.x
- Required Python packages (install via requirements.txt):
  - pandas
  - matplotlib
  - beautifulsoup4
  - jinja2

## Setup and Installation

1. Clone the repository to your local machine or company server.

git clone https://github.com/n740789-am_sangroup/sfdr-report-generator.git

2. Install the required dependencies:

pip install -r requirements.txt

## Usage

1. Place the input Excel files in the `excel_books/aladdin_data/` directory.
2. Run the processing pipeline in order:

python python_scripts/00_data_preper.py
python python_scripts/01_template_builder.py
python python_scripts/02_report_builder.py

3. Generated reports will be available in the `final_reports/` directory.

## Data Processing Pipeline

1. **Data Preparation** (`00_data_preper.py`): Processes and cleans Excel data.
2. **Template Building** (`01_template_builder.py`): Creates HTML templates from configurations.
3. **Report Generation** (`02_report_builder.py`): Produces final HTML reports with visualizations.

## Core Components

The project consists of several Python scripts that work together to process data and generate reports. Here's a detailed overview of each component:

### 1. Data Preparation (00_data_preper.py)
- **Purpose**: Processes and prepares input Excel data for report generation.
- **Key Functions**:
  - Reads Excel files from the `aladdin_data` folder.
  - Processes and cleans data, including handling of special cases and footer indicators.
  - Merges processed data with a master BBDD file.
  - Performs calculations on specific columns (e.g., multiplying values by 100).
  - Generates HTML tables for investments and sector distributions.
  - Sorts and organizes the final DataFrame.
  - Saves the processed data to an Excel file with a date-stamped filename.

### 2. Template Building (01_template_builder.py)
- **Purpose**: Creates HTML templates from narrative configurations.
- **Key Functions**:
  - Reads narrative configurations from an Excel file.
  - Processes each row to create a unique HTML template.
  - Replaces placeholders in the template with actual content.
  - Generates separate templates for different narrative types (e.g., 'sostenible_fi_eq', 'sostenible_fi').

### 3. Report Generation (02_report_builder.py)
- **Purpose**: Generates the final HTML reports by combining processed data with templates.
- **Key Functions**:
  - Reads the processed data Excel file.
  - Matches each data row with the appropriate HTML template.
  - Populates templates with data, including dynamic content like plots and tables.
  - Generates individual HTML reports for each fund/product.

### 4. Plot Building (plot_builder.py)
- **Purpose**: Creates data visualizations for the reports.
- **Key Functions**:
  - Generates horizontal bar charts showing taxonomy alignment for investments.
  - Creates separate charts for scenarios including and excluding sovereign bonds.
  - Handles formatting, coloring, and labeling of charts.
  - Saves generated plots as image files.

### 5. HTML Table Generation (html_table_generator.py)
- **Purpose**: Generates formatted HTML tables for investment and sector data.
- **Key Functions**:
  - Converts pandas DataFrames to HTML tables.
  - Applies custom styling and structure based on table type (investment or sector).
  - Removes unnecessary elements and adds appropriate CSS classes.

## Usage Workflow

1. Place input Excel files in the `excel_books/aladdin_data/` directory.
2. Run `00_data_preper.py` to process and prepare the data.
3. Execute `01_template_builder.py` to generate HTML templates.
4. Run `02_report_builder.py` to create the final HTML reports.

The auxiliary scripts (`plot_builder.py` and `html_table_generator.py`) are called by the main scripts as needed and do not need to be run separately.

## Customizing Reports and Narratives

The content and language of the reports can be customized by editing the narrative configurations in the following Excel file:

./sfdr_report_generator/excel_books/narratives_tables.xlsx

This file contains the text for different sections of the report and supports multiple narratives (e.g., different languages or report styles). To customize:

1. Open the `narratives_tables.xlsx` file.
2. Locate the row corresponding to the narrative you want to edit.
3. Modify the text in the relevant columns to change the content of specific sections in the report.
4. Save the Excel file after making your changes.

The template builder script (`01_template_builder.py`) will use these updated narratives the next time it runs, incorporating your changes into the generated reports.

**Note**: Always make a backup of the Excel file before making significant changes.

## Maintenance and Updates

When adding new features or fixing bugs:
- For data processing changes, modify `00_data_preper.py`.
- For template structure updates, adjust `01_template_builder.py` and the base HTML template.
- For changes in report generation or layout, update `02_report_builder.py`.
- For modifications to charts or plots, edit `plot_builder.py`.
- For changes in table formatting, update `html_table_generator.py`.

Always ensure that changes in one script are reflected in others if they affect the data flow or structure.

## Output

The generated post-contractual reports include:
- Standardized SFDR disclosures
- Data visualizations for key metrics
- Formatted tables for investments and sector distributions
- Responsive HTML layout with company-specific styling

## Internal Use and Sharing

This tool is for internal use within SAM's ESG Global division. It may be shared with different geographical units of our ESG operations but should not be distributed nor shared without permition.

## Support

For support or questions, please contact SAM ESG Global team.

## Confidentiality

This project contains proprietary information. Do not share or distribute this code or documentation outside of authorized company channels.