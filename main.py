import tkinter as tk

"""
class Furnishing(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def create_furnishing(x, y, color):
            self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, outline=color, tags="furnishing")

        def drag_start(event):
            # record item and its location
            self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        def drag_stop(event):
            # reset drag information
            self.drag_data["item"] = None
            self.drag_data["x"] = 0
            self.drag_data["y"] = 0

        def drag(event):
            # compute how much mouse has moved
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            # now move the furnishing
            self.canvas.move(self.drag_data["item"], delta_x, delta_y)
            # record new pos
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        self.canvas = tk.Canvas(width=100, height=100, background="lightyellow")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # used to keep track of a furnishing being dragged
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # example movable object
        create_furnishing(100, 100, "blue")
        create_furnishing(200, 200, "red")

        # bindings for clicking, dragging, and releasing
        self.canvas.tag_bind("furnishing", "<ButtonPress-1>", drag_start)
        self.canvas.tag_bind("furnishing", "<ButtonRelease-1>", drag_stop)
        self.canvas.tag_bind("furnishing", "<B1-Motion>", drag)
"""

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

"""Furnishing(window).pack(fill=tk.BOTH, expand=True)"""
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
