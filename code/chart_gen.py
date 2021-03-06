""" chart_gen.py

Created by 
    name: Callum Johnson
    mail: callum.johnson.aafc@gmail.com

This is a tool created for generating tutoring/coaching score visualisations.
When run, the tool will ask for a set of initial score results, followed by
the set of post-program results.
Upon providing these, two rose charts with score scales will be generated
(one for pre and one for post) as well as a column diagram detailing the
% changes for this student. These images will be saved to the source file
location, as well as being copied to the user's clipboard.

"""

#_______________________________________________________________________________________________________________________
# Global Variables and setup

# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Number of metrics
N_SCORES = 7 

# Total available marks for categories
# (In this case: [English, Art, Maths, History, Sport, Drama, Science])
TOTAL_AVAILABLE = [70,30,40,50,140,50,80]

# In the case of data entry being ordered differently to data presentation (Very company specific, but included nonetheless)
# (In this case we want to order the % Changes as [Maths, History, Art, Sport, English, Drama, Science]) 
PERCENTAGE_ORDERING = [2,3,1,4,0,5,6]

# Similarly for the rose chart we want a new ordering, and also to slightly change the presented labels
ROSE_ORDERING = [3,2,6,0,5,4,1]
ROSE_LABELS = ['History', 'Maths', 'Science', 'English', 'Drama', 'Sport', 'Art']

# Some colouring options
CENTER_WRITING_COL = "#2F326B"
PERCENTAGE_COL = "white"
METRIC_COL = "#00B0F0"
INNER_BORDER_COL = "#323232"
DARK_BLUE = "#2F326B"
GREY = "#808080"

#_______________________________________________________________________________________________________________________
# Main functions

def generate_post_content(old_scores, new_scores):
    """ Generate_Content
    Takes old scores and new scores then generates and saves graphical components.

    Args:
        old_scores (List of floats XOR List of ints): The list of old test scores, 
        can also be already in percentage format (eg. 0.7)
        new_scores (List of floats XOR List of ints): The list of new test scores
    """

    old_pc = get_percentages(old_scores)
    new_pc = get_percentages(new_scores)

    # Generate the rose charts for each set of scores
    generate_rose_chart(old_pc)
    generate_rose_chart(new_pc, suffix = 2)
    # Generate the percentage change graphic
    generate_percentage_change(old_pc,new_pc)

def generate_pre_content(scores, filename = ""):
    """ Generate_Content
    Takes a single set of scores, and generates a rose chart for that scoreset.

    Args:
        scores (List of floats XOR List of ints): The list of test scores, 
        can also be already in percentage format (eg. 0.7)
    """
    # Convert input to percentages
    pc = get_percentages(scores)

    # Generate the rose chart for the results
    generate_rose_chart(pc, filename = filename)

#_______________________________________________________________________________________________________________________
# Helper functions

def get_percentages(scores):
    """ get_percentages
    Formats scores in the order [Mindset,Memory,Processing Info, Notes, Time, Wellbeing, Exams] into a list of floats.

    Args:
        scores ([Str]): A list of strings of either raw scores (eg. 20) or percentages (eg. 0.3).
    """

    # Generate space for percentages
    pc = [0] * N_SCORES

    # Convert each score to a percentage if raw
    for i in range(len(scores)):
        if float(scores[i]) >= 1: pc[i] = int(scores[i])/TOTAL_AVAILABLE[i]
        # Otherwise leave as float
        else: pc[i] = float(scores[i])

    # Return percentages
    return pc

def generate_percentage_change(old_pc,new_pc):
    """ generate_percentage_change
    Generates the graphic showing percentage changes for each focus area.

    Args:
        old_pc (List of Floats): The old percentage scores.
        new_pc (List of Floats): New percentage scores

    Returns:
        plt.Figure : The produced graphic, plotted in matplotlib
    """

    # Calculate changes
    changes= [round(100*(new_pc[i]- old_pc[i])/old_pc[i]) for i in range(N_SCORES)]

    # And overall average change
    avg_change = round(sum(changes)/N_SCORES)

    # Going from [Mindset, Memory, Processing, Notes, Time, Wellbeing, Exams]
    # to [Processing, Notes,Memory, Time, Mindset, Wellbeing, Exams]
    changes = [changes[i] for i in PERCENTAGE_ORDERING]

    # Load template image and generate blank canvas
    img = mpimg.imread('../assets/column_template.png')
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
    plt.savefig("../plots/coltest1.png")
    return fig

def generate_rose_chart(scores, suffix = 1, filename = ""):
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
    results = [results[i] for i in ROSE_ORDERING]


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

    for i in range(n_points):
        ax.text(x=x_coords[i], y= 1 + inner_radius + OFFSET, s=ROSE_LABELS[i],c = "#00B0F0",
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

    # If a custom filename is provided, save it there - otherwise save to plots.
    if filename:
        fig.savefig(f"{filename}.png")
    else:
        fig.savefig(f"../plots/test_chart_{suffix}.png")

#_______________________________________________________________________________

