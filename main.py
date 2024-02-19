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
        window.config(cursor="arrow")
    elif buttonSelected == 2:
        radius = 150
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="green", width=2)
        window.config(cursor="dotbox")
    else:
        length = 50
        canvas.create_rectangle(x-length, y-length, x+length, y+length, outline="orange", width=4)
        window.config(cursor="")


# change cursor for each button type
def set_cursor(event):
    if buttonSelected == 0:
        window.config(cursor="")
    elif buttonSelected == 1:
        window.config(cursor="circle")
    elif buttonSelected == 2:
        window.config(cursor="dotbox")
    else:
        window.config(cursor="question_arrow")
        print("Mouse cursor config error")


# Create window
window = tk.Tk()
window.title("Room Designer")
window.minsize(500, 250)

# set cursor
window.bind("<Enter>", set_cursor)

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
