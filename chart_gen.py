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

#_______________________________________________________________________________________________________________________
# Main function

def generate_post_content(old_scores, new_scores):
    """ Generate_Content
    The main function, takes old scores and new scores then generates and saves
    graphical components.

    Args:
        old_scores (List of floats XOR List of ints): [description]
        new_scores (List of floats XOR List of ints): [description]
    """

    # Total available marks for [Mindset,Memory,Processing Info, Notes, Time, Wellbeing, Exams]
    TOTAL_AVAILABLE = [70,30,40,50,140,50,80]
    
    # If Raw scores are input:
    if float(old_scores[0]) >= 1:
        # Convert raw scores to percentages
        old_pc = [int(old_scores[i])/TOTAL_AVAILABLE[i] for i in range(N_SCORES)]
        new_pc = [int(new_scores[i])/TOTAL_AVAILABLE[i] for i in range(N_SCORES)]
    
    # Otherwise percentages have been used as input, so we convert to float and keep
    else: old_pc, new_pc = [float(i) for i in old_scores], [float(i) for i in new_scores]

    # Generate the rose charts for each set of scores
    generate_rose_chart(old_pc)
    generate_rose_chart(new_pc, suffix = 2)
    # Generate the percentage change graphic
    generate_percentage_change(old_pc,new_pc)

def generate_pre_content(scores):
    """ Generate_Content
    The main function, takes diagnostic scores and saves results as a rose 
    chart.

    Args:
        scores (List of floats XOR List of ints): [description]
    """

    # Total available marks for [Mindset,Memory,Processing Info, Notes, Time, Wellbeing, Exams]
    TOTAL_AVAILABLE = [70,30,40,50,140,50,80]
    
    # If Raw scores are input:
    if float(scores[0]) >= 1:
        # Convert raw scores to percentages
        pc = [int(scores[i])/TOTAL_AVAILABLE[i] for i in range(N_SCORES)]
    
    # Otherwise percentages have been used as input, so we convert to float and keep
    else: pc = [float(i) for i in scores]

    # Generate the rose chart for the results
    generate_rose_chart(pc)

#_______________________________________________________________________________________________________________________
# Helper functions

def generate_percentage_change(old_pc,new_pc):
    """ generate_percentage_change
    Generates the graphic showing percentage changes for each focus area.

    Args:
        old_pc (List of Floats): The old percentage scores.
        new_pc (List of Floats): New percentage scores

    Returns:
        [type]: [description]
    """

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
        ax.text(startx,starty + 198*i, s= f"{changes[i]}%", c = "#2F326B", ha = 'center', va = 'center', size = 9)

    # Add the avg change
    ax.text(400,190,s= f"{avg_change}%", c="#2F326B", ha = 'center', va = 'center')
    # Adjust figure properties then save
    fig.tight_layout()
    #plt.show()
    plt.savefig("plots/coltest1.png")
    return fig

def generate_rose_chart(scores, suffix = 1):
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
    # to ['Notes', 'Processing\nInformation', 'Exams', 'Mindset', 'Wellbeing',
    #  'Time\nManagement', 'Memory']

    new_order = [3,2,6,0,5,4,1]
    results = [results[i] for i in new_order]


    x_min = np.pi/14
    x_max = 2*np.pi
    x_coords = np.linspace(x_min, x_min + x_max, n_points, endpoint=False)
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
    ROTATION_OFFSET = 12.8571429 # pi/14 to degrees
    OFFSET = -0.06 # Offset from top of bar
    for i in range(n_points):
        ax.text(x=x_coords[i], y=results[i] + inner_radius + OFFSET, s=f"{round(100*results[i])}%",c = "white",
                    fontsize = 13.5, # Font size
                    ha = "center", va = "center", # Center justified rotation
                    # Rotation changes over all values
                    rotation = 270 + ROTATION_OFFSET + (i * 360/n_points) if i in [0,1,2,3] \
                        else 90 + ROTATION_OFFSET + (i * 360/n_points))

    # Add Titles
    OFFSET = 0.15 # Offset from circle edge

    # Metrics
    METRICS = ['Notes', 'Processing\nInformation', 'Exams', 'Mindset', 'Wellbeing', 'Time\nManagement', 'Memory']
    for i in range(n_points):
        ax.text(x=x_coords[i], y= 1 + inner_radius + OFFSET, s=METRICS[i],c = "#00B0F0",
                    fontsize = 16, # Font size
                    ha = "center", va = "center", # Center justified rotation
                    # Rotation changes over all values
                    rotation = 270 + ROTATION_OFFSET + (i * 360/n_points) if i in [0,1,2,3] \
                        else 90 + ROTATION_OFFSET + (i * 360/n_points))

    # Center writing
    ax.text(x=0,y=0, s="Study profile", c = CENTER_WRITING_COL,
            fontsize = 16,
            ha = "center", va = "center")

    plt.axis("off")
    fig.savefig(f"plots/test_chart_{suffix}.png")
    # plt.show()

# print("Hello there.")
# old_scores = input("Please enter the original scores, separated by commas, in the following order: Mindset, Memory, Processing Info, Notes, Time, Wellbeing, Exams\n")
# new_scores = input("Now enter the new scores:\n")
# generate_content(old_scores.split(','),new_scores.split(','))
