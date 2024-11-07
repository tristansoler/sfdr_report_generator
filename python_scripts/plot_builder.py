import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_plot(row_data, output_dir, report_id):
    # Function to create data for a single chart
    def prepare_data(row, include_sov):
        suffix = "" if include_sov else "_exsovereign"
        data = {
            "Volumen de\nnegocios": {
                "gas": row[f"total_turnover_gas{suffix}"],
                "nuclear": row[f"total_turnover_nuclear{suffix}"],
                "nogasnonuclear": row[f"total_turnover_nogasnonuclear{suffix}"],
                "rest": row[
                    f"rest_turnover_aligned{suffix}"
                ],  # need to modify "rest", we don't get it anymore
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

    # Prepare data for both charts
    data_with_sb = prepare_data(row_data, True)
    data_without_sb = prepare_data(row_data, False)

    # Function to create a single chart
    def create_chart(ax, data, title):
        categories = ["Volumen de\nnegocios", "CapEx", "OpEx"]
        cumulative = np.zeros(len(categories))
        colors = ["#98fb98", "#2e8b57", "#1a472a", "#d3d3d3"]
        labels = [
            "Taxonomía alineada: gas fósil",
            "Taxonomía alineada: nuclear",
            "Taxonomía alineada: (sin gas y nuclear)",
            "No alineado",
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
        ax.set_xlabel("Porcentaje")
        ax.set_title(title)

        # Remove all spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Add percentage labels
        for i, category in enumerate(categories):
            cumsum = 0
            small_values = []
            for j, column in enumerate(["gas", "nuclear", "nogasnonuclear", "rest"]):
                width = data[category][column]
                if width > 0:
                    if width < 10 or (
                        j == 2 and width < 15
                    ):  # Condition for small values including 'sin gas y nuclear'
                        small_values.append((width, j, cumsum))
                    else:  # For larger values, keep the annotation inside the bar
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

            # Sort small values from larger to smaller
            small_values.sort(reverse=True)

            # Add annotations for small values
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

        # Adjust y-axis to make room for labels
        ax.set_ylim(-1.5, len(categories) - 0.5)

        # Adjust y-tick labels
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(
            categories[::-1]
        )  # Reverse the order to match the desired layout

    # Create the figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

    # Create both charts
    create_chart(
        ax1,
        data_with_sb,
        "1. Ajuste a la taxonomía de las inversiones,\nincluidos los bonos soberanos*",
    )
    create_chart(
        ax2,
        data_without_sb,
        "2. Ajuste a la taxonomía de las inversiones,\nexcluidos los bonos soberanos*",
    )

    # Add a common legend
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=4)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Save the plot
    plot_filename = f"plot_{report_id}.png"
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    return plot_filename


# Example usage (commented out)
# if __name__ == "__main__":
#     excel_path = "path/to/your/excel/file.xlsx"
#     output_dir = "path/to/output/directory"
#     report_id = "example_report"
#     plot_filename = build_plot(excel_path, output_dir, report_id)
#     print(f"Plot saved as: {plot_filename}")
