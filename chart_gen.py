""" chart_gen.py

Created by 
    name: Callum Johnson
    mail: callum.johnson.aafc@gmail.com

This is a tool created for generating elevate graduation pack visualisations.
When run, the tool will ask for a set of initial score results, followed by
the set of post diagnostic results.
Upon providing these, two rose charts with score scales will be generated
(one for pre and one for post) as well as a column diagram detailing the
% changes for this student. These images will be saved to the source file
location.

"""
# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Global Variables
N_SCORES = 7
CENTER_WRITING_COL = "#2F326B"
PERCENTAGE_COL = "white"
METRIC_COL = "#00B0F0"
INNER_BORDER_COL = "#323232"
DARK_BLUE = "#2F326B"
GREY = "#808080"

def generate_content(old_scores, new_scores):

    # Total available marks for [Mindset,Memory,Processing Info, Notes, Time, Wellbeing, Exams]
    TOTAL_AVAILABLE = [70,30,40,50,140,50,80]
    
    # Convert raw scores to percentages
    old_pc = [old_scores[i]/TOTAL_AVAILABLE[i] for i in range(N_SCORES)]
    new_pc = [new_scores[i]/TOTAL_AVAILABLE[i] for i in range(N_SCORES)]
    generate_rose_chart(old_pc)
    generate_rose_chart(new_pc)
    generate_percentage_change(old_pc,new_pc)

def generate_percentage_change(old_pc,new_pc):

    # Calculate changes
    changes= [round(100*(new_pc[i]- old_pc[i])/old_pc[i]) for i in range(N_SCORES)]
    # And overall average change
    avg_change = round(sum(changes)/N_SCORES)

    # Going from [Mindset, Memory, Processing, Notes, Time, Wellbeing, Exams]
    # to [Processing, Notes,Memory, Time, Mindset, Wellbeing, Exams]
    new_order = [2,3,1,4,0,5,6]
    changes = [changes[i] for i in new_order]

    # Load template image and generate blank canvas
    img = mpimg.imread('assets/column_template.png')
    fig, ax = plt.subplots(dpi=500)
    ax.axis('off')
    # Add the figure
    ax.imshow(img)

    # Add each of the % changes
    startx = 560
    starty = 410
    for i in range(N_SCORES):
        ax.text(startx,starty + 198*i, s= f"{changes[i]}%", c = "#2F326B", ha = 'center', va = 'center', size = 8)

    # Add the avg change
    ax.text(400,190,s= f"{avg_change}%", c="#2F326B", ha = 'center', va = 'center')
    # Adjust figure properties then save
    fig.tight_layout()
    plt.show()
    plt.savefig("plots/coltest1.png")
    return fig

def generate_rose_chart(scores):
    """
    Generates a rose chart for a single set of results.

    Args:
        scores (Int, Float): Can be either raw scores or percentage scores.
    """
    #___________________________________________________________________________
    # Chart Setup
    n_points = 7
    inner_radius = 0.35

    # White background / Blue outer ring
    background = [1] * n_points

    # Results
    results = np.array(scores)

    # Going from [Mindset, Memory, Processing, Notes, Time, Wellbeing, Exams]
    # to [Processing, Notes,Memory, Time, Mindset, Wellbeing, Exams]
    new_order = [2,3,1,4,0,5,6]
    results = [results[i] for i in new_order]

    # Now need to 'spin the wheel' to match original format
    # new_order = [4,0,5,6,2,3,1]
    # results = [results[i] for i in new_order]

    x_max = 2*np.pi
    x_coords = np.linspace(0, x_max, n_points, endpoint=False)
    width = x_max / n_points

    #___________________________________________________________________________
    # Plotting

    # Generate blank figure
    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)

    # Plot Background
    ax.bar(
        x_coords,
        background,
        width=width,
        bottom=inner_radius,
        color="white",
        edgecolor="white",
        linewidth=3
    )
    # Plot Results
    ax.bar(
        x_coords,
        results,
        width=width,
        bottom=inner_radius,
        color="#2F326B",
        edgecolor="#808080",
        linewidth=1
    )

    # Plot grey lines
    ax.bar(
        x_coords,
        background,
        width=width,
        bottom=inner_radius,
        fill = False,
        edgecolor="#808080",
        linewidth=1
    )

    # Plot outer ring
    n_border_points = 1000
    border_points = np.linspace(0, x_max, n_border_points, endpoint=False)
    ax.plot(border_points, [1 + inner_radius] * n_border_points, c = "#2F326B", linewidth = 4)

    # Plot Inner ring
    ax.plot(border_points, [inner_radius] * n_border_points, c = INNER_BORDER_COL, linewidth = 6)

    #___________________________________________________________________________
    # Adding Text and Titles

    # Add Percentages
    OFFSET = -0.06 # Offset from top of bar
    for i in range(n_points):
        ax.text(x=x_coords[i], y=results[i] + inner_radius + OFFSET, s=f"{round(100*results[i])}%",c = "white",
                    fontsize = 13.5, # Font size
                    ha = "center", va = "center", # Center justified rotation
                    # Rotation changes over all values
                    rotation = 270 + (i * 360/n_points) if i in [0,1,2,3] else 90 + (i * 360/n_points))

    # Add Titles
    OFFSET = 0.1
    # Metrics
    METRICS = ["Mindset","Memory","Processing\nInformation", "Notes", "Time", "Wellbeing", "Exams"]
    for i in range(n_points):
        ax.text(x=x_coords[i], y= 1 + inner_radius + OFFSET, s=METRICS[i],c = "#00B0F0",
                    fontsize = 15, # Font size
                    ha = "center", va = "center", # Center justified rotation
                    # Rotation changes over all values
                    rotation = 270 + (i * 360/n_points) if i in [0,1,2,3] else 90 + (i * 360/n_points))

    # Center writing
    ax.text(x=0,y=0, s="Study profile", c = CENTER_WRITING_COL,
            fontsize = 16,
            ha = "center", va = "center")

    plt.axis("off")
    fig.savefig("plots/test_chart.png")
    plt.show()
