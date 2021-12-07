import tkinter as tk
from chart_gen import *
from copy_to_clipboard import *

# Function Call for the 'Generate!' button
def callback(boxes):
    scores = [box.get() for box in boxes]
    generate_pre_content(scores, filename = "results")
    send_to_clipboard(f"results.png")

# Main driver
def main():
    METRICS = ["Mindset", "Memory", "Processing", "Notes", "Time", "Wellbeing", "Exams"]
    window = tk.Tk()
    # Set the window title
    window.title("chart_gen")
    
    # Create and pack a greeting
    tk.Label(text="Hello! Welcome to chart_gen by Callum Johnson", background = "#34A2FE").pack()

    # Create labels and input boxes
    labels = [tk.Label(text=m) for m in METRICS]
    boxes = [tk.Entry() for i in METRICS]
    # Pack all components into window
    for i in range(len(METRICS)):
        labels[i].pack()
        boxes[i].pack()

    # Add instructions
    tk.Label(text = "Click below or hit enter to copy results to clipboard", pady= 6).pack()

    # Add a button to generate underneath
    button = tk.Button(text="Generate!", command = lambda: callback(boxes))
    button.pack()

    # Also allow hitting the enter key to generate results
    window.bind('<Return>', (lambda event: callback(boxes)))

    # And finally bind the closing of the window to exiting the program
    def on_closing():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()