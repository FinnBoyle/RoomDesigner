import tkinter as tk

buttonSelected = 0


def update_selected(value):
    global buttonSelected
    buttonSelected = value


def button_select(event):
    global buttonSelected
    x = event.x
    y = event.y
    if buttonSelected == 1:
        radius = 75
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="red", width=2)
    elif buttonSelected == 2:
        radius = 150
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="green", width=2)
    else:
        length = 50
        canvas.create_rectangle(x-length, y-length, x+length, y+length, outline="orange", width=4)


def set_cursor(event):
    window.config(cursor="top_left_arrow")


def reset_cursor(event):
    window.config(cursor="")


# Create window
window = tk.Tk()
window.title("Room Designer")
window.minsize(500, 250)

# Cursor testing
window.bind("<Enter>", set_cursor)
window.bind("<Leave>", reset_cursor)

# Create button panel, and buttons in panel
buttons = tk.Frame(window, bg="lightgreen", borderwidth=7.5, highlightbackground="black", highlightthickness=1)
buttons.pack(fill=tk.Y, side=tk.LEFT)

buildWalls = tk.Button(master=buttons, text="Build Walls", width=10, bg="lightblue",
                       command=lambda: update_selected(1))
buildWalls.pack()
addFurnishings = tk.Button(master=buttons, text="Add\nFurnishing", width=10, bg="lightblue",
                           command=lambda: update_selected(2))
addFurnishings.pack()
removeEither = tk.Button(master=buttons, text="Remove\nWalls/\nFurnishing", width=10, bg="lightblue",
                         command=lambda: update_selected(0))
removeEither.pack()


# Components to be added to workspace
canvas = tk.Canvas(window, width=100, height=100, bg="lightyellow")
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", button_select)

# Build GUI
window.mainloop()
