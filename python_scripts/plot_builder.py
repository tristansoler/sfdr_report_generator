import json
import logging
import os
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def build_plot(row_data, output_dir, report_id, translations, input_language):
    # Function to translate text based on the input language
    def translate(text, lang, trans=translations):
        if lang == "en":
            return text
        translated = trans.get(lang, {}).get(text, text)
        if translated == text:
            logging.warning(f"No translation found for '{text}' in language '{lang}'")
        return translated

    # Function to prepare data for plotting
    def prepare_data(row, include_sov):
        suffix = "" if include_sov else "_exsovereign"
        data = {
            translate("Turnover", input_language): {
                "gas": row[f"total_turnover_gas{suffix}"],
                "nuclear": row[f"total_turnover_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_turnover_nogasnonuclear{suffix}"],
                "rest": row[f"rest_turnover_aligned{suffix}"],
            },
            "CapEx": {
                "gas": row[f"total_capex_gas{suffix}"],
                "nuclear": row[f"total_capex_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_capex_nogasnonuclear{suffix}"],
                "rest": row[f"rest_opex_aligned{suffix}"],
            },
            "OpEx": {
                "gas": row[f"total_opex_gas{suffix}"],
                "nuclear": row[f"total_opex_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_opex_nogasnonuclear{suffix}"],
                "rest": row[f"rest_capex_aligned{suffix}"],
            },
        }
        return pd.DataFrame(data)

    # Prepare data with and without sovereign bonds
    data_with_sb = prepare_data(row_data, True)
    data_without_sb = prepare_data(row_data, False)

    # add total investments to the data without sovereign bonds
    # total investments is  portfolio_mv_exsov in the row data
    data_without_sb["total_investments"] = row_data["portfolio_mv_exsov"]

    # Translate the total investments string
    STRING_TOT_INVESTMENTS = translate(
        "This graph represents x_subs% of the total investments.", input_language
    )
    UPDATED_STRING = STRING_TOT_INVESTMENTS.replace(
        "x_subs", f"{data_without_sb['total_investments'].iloc[0] * 100:.1f}"
    )

    # Function to create a chart
    def create_chart(ax, data, title, input_language=input_language):
        categories = [
            translate("Turnover", input_language),
            "CapEx",
            "OpEx",
        ]
        columns = ["gas", "nuclear", "nogasnonuclear", "rest"]
        colors = [
            "#7d9a7e",  # light green
            "#4d734f",  # med green
            "#013300",  # dark green
            "#dadada",  # grey
        ]
        labels = [
            translate("Taxonomy-aligned: Fossil gas", input_language),
            translate("Taxonomy-aligned: Nuclear", input_language),
            translate("Taxonomy-aligned (no gas and nuclear)", input_language),
            translate("Non Taxonomy-aligned", input_language),
        ]

        bar_height = 0.3  # Set bar height; stick to 0.3; 0.5 is too wide

        # Create horizontal stacked bar chart and optimize annotations
        for i, category in enumerate(categories):
            cumulative = 0
            total = sum(data[category][col] for col in columns)
            small_values = []

            for j, column in enumerate(columns):
                value = data[category][column]
                width = (value / total) * 100 if total > 0 else 0

                ax.barh(
                    category,
                    width,
                    left=cumulative,
                    color=colors[j],
                    label=labels[j] if i == 0 else "",
                    height=bar_height,
                )

                if width > 0:
                    if width < 10 or (j == 2 and width < 15):
                        small_values.append((width, j, cumulative))
                    else:
                        ax.annotate(
                            f"{width:.2f}%",
                            xy=(cumulative + width / 2, i),
                            xytext=(0, 0),
                            textcoords="offset points",
                            va="center",
                            ha="center",
                            color="white",
                            fontweight="bold",
                            fontsize=15,  # it was 10 and I changed it to 15
                        )

                cumulative += width

            # Handle small value annotations
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
                    fontsize=14,
                    arrowprops=dict(
                        arrowstyle="-",
                        color=colors[j],
                        lw=0.5,
                        connectionstyle="angle,angleA=0,angleB=90,rad=3",
                    ),
                )

        # Set chart properties
        ax.set_xlim(0, 100)
        ax.set_xticks(range(0, 101, 25))
        ax.set_xlabel(translate("Percentage", input_language), fontsize=14)
        wrapped_title = "\n".join(wrap(title, width=40))
        ax.set_title(wrapped_title, fontsize=24, wrap=True)

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Set y-axis properties
        ax.set_ylim(-0.8, len(categories) - 0.2)
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories[::-1], fontsize=22)  # define ylable size here

        return ax.get_legend_handles_labels()

    # Create the figure with two subplots / edit plot size here
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 8))

    # Add a vertical line between the subplots
    fig.subplots_adjust(wspace=0.5)  # Adjust space between subplots if necessary
    line_x = (ax1.get_position().x1 + ax2.get_position().x0) / 2
    line = Line2D(
        [line_x, line_x],
        [-0.15, 1],
        transform=fig.transFigure,
        color="#fae8d4",
        linewidth=2,
        clip_on=True,  # Added to allow the line to extend beyond the figure
    )
    fig.add_artist(line)

    # Create charts for data with and without sovereign bonds
    handles1, labels1 = create_chart(
        ax1,
        data_with_sb,
        title=translate(
            "1. Taxonomy-alignment of investments including sovereign bonds*",
            input_language,
        ),
    )
    handles2, labels2 = create_chart(
        ax2,
        data_without_sb,
        title=translate(
            "2. Taxonomy-alignment of investments excluding sovereign bonds*",
            input_language,
        ),
    )

    # Add legends to the subplots
    ax1.legend(
        handles1,
        labels1,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),  # Moved up from -0.15
        ncol=1,
        fontsize=22,
        frameon=False,
        columnspacing=1,  # Add spacing between columns
        handletextpad=0.5,  # Reduce space between handle and text
    )  # Create separate legends for each subplot
    ax2.legend(
        handles2,
        labels2,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),  # Moved up from -0.15
        ncol=1,
        fontsize=22,
        frameon=False,
        columnspacing=1,  # Add spacing between columns
        handletextpad=0.5,  # Reduce space between handle and text
    )

    # Add the UPDATED_STRING below the legend of ax2
    fig.text(
        0.75, -0.15, UPDATED_STRING, ha="center", va="bottom", fontsize=22, wrap=True
    )

    # Adjust layout and spacing
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3, wspace=0.5)  # Adjusted from 0.3 to 0.2

    # Save the plot
    plot_filename = f"plot_{report_id}.png"
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(
        plot_path, bbox_inches="tight", dpi=300
    )  # Increased DPI for better quality

    # logg where the plot was saved
    logging.info(f"Plot saved to: {plot_path}")

    # Close the plot to free up memory
    plt.close()

    return plot_filename
