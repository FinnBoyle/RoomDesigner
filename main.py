import math
import tkinter as tk

buttonSelected = 0


def create_furnishing(color, x, y):
    canvas.create_polygon(x - 25, y - 25, x + 25, y - 25, x + 25, y + 25, x - 25, y + 25, outline=color,
                          fill="lightyellow", width=10, tags="furnishing")


def delete_furnishing(event):
    canvas.delete(canvas.find_closest(event.x, event.y))


def rotate_furnishing(clockwise, event):
    if clockwise:
        amount = 0.087  # 5 degrees in radians
    else:
        amount = -0.087  # -5 degrees in radians

    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    selected = canvas.find_closest(x, y)[0]
    coordinates = find_vertices(selected)
    centre_x = sum(x for x, y in coordinates) / len(coordinates)
    centre_y = sum(y for x, y in coordinates) / len(coordinates)

    canvas.delete(selected)

    rotated_coords = []
    for x, y in coordinates:
        x_rotated = centre_x + (x - centre_x) * math.cos(amount) - (y - centre_y) * math.sin(amount)
        y_rotated = centre_y + (x - centre_x) * math.sin(amount) + (y - centre_y) * math.cos(amount)
        rotated_coords.append((x_rotated, y_rotated))

    canvas.create_polygon(*sum(rotated_coords, ()), outline="black", fill="lightyellow", width=10, tags="furnishing")


def find_vertices(selected):
    coordinates = canvas.coords(selected)

    return [(coordinates[i], coordinates[i + 1]) for i in range(0, len(coordinates), 2)]


def drag_start(event):
    # record item and its location
    move_drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    move_drag_data["x"] = event.x
    move_drag_data["y"] = event.y


def drag_stop(event):
    # reset drag information
    move_drag_data["item"] = None
    move_drag_data["x"] = 0
    move_drag_data["y"] = 0


def drag(event):
    # compute how much mouse has moved
    delta_x = event.x - move_drag_data["x"]
    delta_y = event.y - move_drag_data["y"]
    # now move the furnishing
    canvas.move(move_drag_data["item"], delta_x, delta_y)
    # record new pos
    move_drag_data["x"] = event.x
    move_drag_data["y"] = event.y


"""
def resize_start(event):
    global resize_dragging
    resize_dragging = True
    resize_drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    resize_drag_data["x"] = event.x
    resize_drag_data["y"] = event.y


def resize_stop(event):
    global resize_dragging
    resize_dragging = False
    resize_drag_data["item"] = None
    resize_drag_data["x"] = 0
    resize_drag_data["y"] = 0


def drag_resize(event):
    global resize_dragging
    coordinates = find_vertices(resize_drag_data["item"])

    if resize_dragging:
        delta_x = event.x - resize_drag_data["x"]
        delta_y = event.y - resize_drag_data["y"]

        new_size = []
        for x, y in coordinates:
            new_x = x + delta_x
            new_y = y + delta_y
            new_size.append((new_x, new_y))

        canvas.coords(resize_drag_data["item"], *sum(new_size, ()))

        resize_drag_data["x"] = event.x
        resize_drag_data["y"] = event.y
"""


def update_selected(value):
    global buttonSelected
    buttonSelected = value


def button_select(event):
    global buttonSelected
    x = event.x
    y = event.y
    if buttonSelected == 1:
        create_furnishing("darkgreen", x, y)
        window.config(cursor="arrow")
    elif buttonSelected == 2:
        create_furnishing("lightgreen", x, y)
        window.config(cursor="dotbox")
    else:
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
window.minsize(1000, 500)

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

removeEither = tk.Button(master=buttons, text="Pointer", width=10, bg="lightblue",
                         command=lambda: update_selected(0))
removeEither.pack()

message = tk.Label(master=buttons, text="Left click\nto add and\ndrag, right\nclick to\ndelete", width=10, bg="white")
message.pack(pady=5)

message2 = tk.Label(master=buttons, text="Right/left\narrow keys to\nrotate items\nclockwise/\nanticlockwise")
message2.pack()

# Components to be added to workspace
canvas = tk.Canvas(window, width=500, height=250, bg="lightyellow")
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", button_select)

# used to keep track of a furnishing being dragged
move_drag_data = {"x": 0, "y": 0, "item": None}
"""
resize_dragging = False
resize_drag_data = {"x": 0, "y": 0, "item": None}
"""

# bound events
canvas.focus_set()
canvas.tag_bind("furnishing", "<ButtonPress-3>", delete_furnishing)  # right click
canvas.tag_bind("furnishing", "<ButtonPress-1>", drag_start)  # left click
canvas.tag_bind("furnishing", "<ButtonRelease-1>", drag_stop)  # left click
canvas.tag_bind("furnishing", "<B1-Motion>", drag)  # left click
canvas.bind("<Left>", lambda event: rotate_furnishing(False, event))  # left arrow
canvas.bind("<Right>", lambda event: rotate_furnishing(True, event))

# Build GUI
window.mainloop()
