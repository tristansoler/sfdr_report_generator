import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
df = pd.read_excel(r'C:\Users\n740789\Documents\sfdr_report_generator\excel_books\test_plot_builder.xlsx')

# Function to create data for a single chart
def prepare_data(df, include_sb):
    suffix = '' if include_sb else '_sbexcluded'
    data = {
        'Volumen de\nnegocios': {
            'gas': df[f'total_turnover_gas{suffix}'].values[0],
            'nuclear': df[f'total_turnover_nuclear{suffix}'].values[0],
            'nogasnonuclear': df[f'total_turnover_nogasnonuclear{suffix}'].values[0],
            'rest': df[f'total_turnover_rest{suffix}'].values[0]
        },
        'CapEx': {
            'gas': df[f'total_capex_gas{suffix}'].values[0],
            'nuclear': df[f'total_capex_nuclear{suffix}'].values[0],
            'nogasnonuclear': df[f'total_capex_nogasnonuclear{suffix}'].values[0],
            'rest': df[f'total_capex_rest{suffix}'].values[0]
        },
        'OpEx': {
            'gas': df[f'total_opex_gas{suffix}'].values[0],
            'nuclear': df[f'total_opex_nuclear{suffix}'].values[0],
            'nogasnonuclear': df[f'total_opex_nogasnonuclear{suffix}'].values[0],
            'rest': df[f'total_opex_rest{suffix}'].values[0]
        }
    }
    return pd.DataFrame(data).transpose()

# Prepare data for both charts
data_with_sb = prepare_data(df, True)
data_without_sb = prepare_data(df, False)

# Function to create a single chart
def create_chart(ax, data, title):
    categories = list(data.index)
    cumulative = np.zeros(len(categories))
    colors = ['#98fb98', '#2e8b57', '#1a472a', '#d3d3d3']
    labels = ['Taxonomía alineada: gas fósil', 'Taxonomía alineada: nuclear', 
              'Taxonomía alineada: (sin gas y nuclear)', 'No alineado']

    bar_height = 0.3  # Adjust this value to change the thickness of the bars

    for i, column in enumerate(data.columns):
        values = data[column]
        ax.barh(categories, values, left=cumulative, color=colors[i], label=labels[i], height=bar_height)
        cumulative += values

    ax.set_xlim(0, 100)
    ax.set_xlabel('Porcentaje')
    ax.set_title(title)
    
    # Remove all spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add percentage labels
    for i, category in enumerate(categories):
        cumsum = 0
        small_values = []
        for j, column in enumerate(data.columns):
            width = data.loc[category, column]
            if width > 0:
                if width < 10 or (j == 2 and width < 15):  # Condition for small values including 'sin gas y nuclear'
                    small_values.append((width, j, cumsum))
                else:  # For larger values, keep the annotation inside the bar
                    ax.annotate(f'{width:.2f}%', 
                                xy=(cumsum + width/2, i),
                                xytext=(0, 0),
                                textcoords='offset points',
                                va='center',
                                ha='center',
                                color='white',
                                fontweight='bold',
                                fontsize=8)
            cumsum += width
        
        # Sort small values from larger to smaller
        small_values.sort(reverse=True)
        
        # Add annotations for small values
        for idx, (width, j, start) in enumerate(small_values):
            ax.annotate(f'{width:.2f}%', 
                        xy=(start + width/2, i),
                        xytext=(5, -20 - idx * 15),
                        textcoords='offset points',
                        va='top',
                        ha='left',
                        color=colors[j],
                        fontweight='bold',
                        fontsize=8,
                        arrowprops=dict(arrowstyle='-', color=colors[j], lw=0.5, 
                                        connectionstyle="angle,angleA=0,angleB=90,rad=3"))

    # Adjust y-axis to make room for labels
    ax.set_ylim(-1.5, len(categories) - 0.5)

    # Adjust y-tick labels
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))  # Set to (10, 6) as requested

# Create both charts
create_chart(ax1, data_with_sb, '1. Ajuste a la taxonomía de las inversiones,\nincluidos los bonos soberanos*')
create_chart(ax2, data_without_sb, '2. Ajuste a la taxonomía de las inversiones,\nexcluidos los bonos soberanos*')

# Add a common legend
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=4)

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()