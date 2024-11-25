import os
import logging
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load translations
with open(
    r"C:\Users\n740789\Documents\sfdr_report_generator\python_scripts\translations.json",
    "r",
    encoding="utf-8",
) as f:
    translations = json.load(f)

# Ask for user input for language
try:
    input_language = input("Enter the language code (es, en, pt, or pl): ")
    if not isinstance(input_language, str) or input_language not in [
        "es",
        "en",
        "pt",
        "pl",
    ]:
        raise ValueError(
            "Invalid language code. Please enter 'es', 'en', 'pt', or 'pl'."
        )
except ValueError as e:
    print(e)
    logging.error(e)


# Function to translate text
def translate(text, lang):
    if lang == "en":
        return text
    return translations.get(lang, {}).get(text, text)


def build_plot(row_data, output_dir, report_id):
    def prepare_data(row, include_sov):
        suffix = "" if include_sov else "_exsovereign"
        data = {
            translate("Turnover", input_language): {
                "gas": row[f"total_turnover_gas{suffix}"],
                "nuclear": row[f"total_turnover_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_turnover_nogasnonuclear{suffix}"],
                "rest": row[f"rest_turnover_aligned{suffix}"],
            },
            translate("CapEx", input_language): {
                "gas": row[f"total_capex_gas{suffix}"],
                "nuclear": row[f"total_capex_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_capex_nogasnonuclear{suffix}"],
                "rest": row[f"rest_opex_aligned{suffix}"],
            },
            translate("OpEx", input_language): {
                "gas": row[f"total_opex_gas{suffix}"],
                "nuclear": row[f"total_opex_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_opex_nogasnonuclear{suffix}"],
                "rest": row[f"rest_capex_aligned{suffix}"],
            },
        }
        return pd.DataFrame(data)

    data_with_sb = prepare_data(row_data, True)
    data_without_sb = prepare_data(row_data, False)

    STRING_TOT_INVESTMENTS = translate(
        "This graph represents x% of the total investments.", input_language
    )
    # UPDATED_STRING = STRING_TOT_INVESTMENTS.replace(
    #    "x", str(data_without_sb["total_investments"][0])
    # )

    def create_chart(ax, data, title):
        categories = [
            translate("Turnover", input_language),
            translate("CapEx", input_language),
            translate("OpEx", input_language),
        ]
        cumulative = np.zeros(len(categories))
        # WE NEED TO CHANGE THE COLORS  SO THEY LOOK MORE LIKE THE EU SAMPLE
        colors = [
            "#98fb98",
            "#2e8b57",
            "#1a472a",
            "#d3d3d3",
        ]
        labels = [
            translate("Taxonomy-aligned: Fossil gas", input_language),
            translate("Taxonomy-aligned: Nuclear", input_language),
            translate("Taxonomy-aligned (no gas and nuclear)", input_language),
            translate("Non Taxonomy-aligned", input_language),
        ]

        bar_height = 0.3  # Adjust this value to change the thickness of the bars

        for i, column in enumerate(["gas", "nuclear", "nogasnonuclear", "rest"]):
            values = [data[cat][column] for cat in categories]
            ax.barh(
                categories,
                values,
                left=cumulative,
                color=colors[i],
                label=labels[i],
                height=bar_height,
            )
            cumulative += values

        ax.set_xlim(0, 100)
        ax.set_xlabel(translate("Percentage", input_language))
        ax.set_title(title)

        for spine in ax.spines.values():
            spine.set_visible(False)

        for i, category in enumerate(categories):
            cumsum = 0
            small_values = []
            for j, column in enumerate(["gas", "nuclear", "nogasnonuclear", "rest"]):
                width = data[category][column]
                if width > 0:
                    if width < 10 or (j == 2 and width < 15):
                        small_values.append((width, j, cumsum))
                    else:
                        ax.annotate(
                            f"{width:.2f}%",
                            xy=(cumsum + width / 2, i),
                            xytext=(0, 0),
                            textcoords="offset points",
                            va="center",
                            ha="center",
                            color="white",
                            fontweight="bold",
                            fontsize=8,
                        )
                cumsum += width

            small_values.sort(reverse=True)

            for idx, (width, j, start) in enumerate(small_values):
                ax.annotate(
                    f"{width:.2f}%",
                    xy=(start + width / 2, i),
                    xytext=(5, -20 - idx * 15),
                    textcoords="offset points",
                    va="top",
                    ha="left",
                    color=colors[j],
                    fontweight="bold",
                    fontsize=8,
                    arrowprops=dict(
                        arrowstyle="-",
                        color=colors[j],
                        lw=0.5,
                        connectionstyle="angle,angleA=0,angleB=90,rad=3",
                    ),
                )

        ax.set_ylim(-1.5, len(categories) - 0.5)
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories[::-1])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

    create_chart(
        ax1,
        data_with_sb,
        title=translate(
            "1. Taxonomy-alignment of investments including sovereign bonds*",
            input_language,
        ),
    )
    create_chart(
        ax2,
        data_without_sb,
        title=translate(
            "2. Taxonomy-alignment of investments excluding sovereign bonds*",
            input_language,
        ),
    )

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=4)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    plot_filename = f"plot_{report_id}.png"
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)

    # logg where the plot was saved
    logging.info(f"Plot saved to: {plot_path}")

    plt.close()

    return plot_filename
