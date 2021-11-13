import tkinter as tk
from chart_gen import *

def callback(boxes, f):
    print("Running")
    scores = [box.get() for box in boxes]
    generate_pre_content(scores, filename = f.get())
    print("Complete.")

def main():
    METRICS = ["Mindset", "Memory", "Processing", "Notes", "Time", "Wellbeing", "Exams"]
    window = tk.Tk()
    greeting = tk.Label(text="Hello!, Welcome to chart_gen", background = "#34A2FE")

    # Create labels and input boxes
    labels = [tk.Label(text=m) for m in METRICS]
    boxes = [tk.Entry() for i in METRICS]
    # Pack all components into window
    greeting.pack()
    for i in range(len(METRICS)):
        labels[i].pack()
        boxes[i].pack()
    # Add an option to include a filename
    filereq = tk.Label(text= "OPTIONAL: Name your file below")
    filebox = tk.Entry()
    filereq.pack()
    filebox.pack()
    # Add a button to generate underneath
    button = tk.Button(text="Generate!", command = lambda: callback(boxes, filebox))
    button.pack()

    window.mainloop()