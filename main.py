import tkinter as tk

# Create window
window = tk.Tk()
window.title("Room Designer")
window.minsize(500, 250)

# Create button panel, and buttons in panel
buttons = tk.Frame(window, bg="lightgreen", borderwidth=7.5, highlightbackground="black", highlightthickness=1)
buttons.pack(fill=tk.Y, side=tk.LEFT)

buildWalls = tk.Button(master=buttons, text="Build Walls", width=10, bg="lightblue")
buildWalls.pack()
addFurnishings = tk.Button(master=buttons, text="Add\nFurnishing", width=10, bg="lightblue")
addFurnishings.pack()
removeEither = tk.Button(master=buttons, text="Remove\nWalls/\nFurnishing", width=10, bg="lightblue")
removeEither.pack()

# Components added here
workspace = tk.Frame(window, bg="lightyellow")
workspace.pack(fill=tk.BOTH, expand=True)

# To remove...
canvas = tk.Canvas(workspace, width=100, height=100, bg="lightyellow")
canvas.pack()
canvas.create_oval(25, 25, 75, 75, width=10, fill="black")

# Build GUI
window.mainloop()
