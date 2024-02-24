import math
import tkinter as tk

buttonSelected = 0


def create_furnishing(mult, x, y):
    canvas.create_polygon(x - mult * 25, y - mult * 25, x + mult * 25, y - mult * 25, x + mult * 25, y + mult * 25,
                          x - mult * 25, y + mult * 25, outline="black", fill="lightyellow", width=10,
                          tags="furnishing")


def delete_furnishing(event):
    canvas.delete(canvas.find_closest(event.x, event.y))


# BUGGED, cause would be 'coordinates' values, should probably change everything to polygons instead of rectangles?
def rotate_furnishing(event):
    x = event.x
    y = event.y

    selected = canvas.find_closest(x, y)[0]
    coordinates = find_vertices(selected)
    centre_x = sum(x for x, y in coordinates) / len(coordinates)
    centre_y = sum(y for x, y in coordinates) / len(coordinates)

    dx = x - centre_x
    dy = y - centre_y

    angle_radians = math.atan2(dy, dx)

    canvas.delete(selected)

    rotated_coords = []
    for x, y in coordinates:
        x_rotated = centre_x + (x - centre_x) * math.cos(angle_radians) - (y - centre_y) * math.sin(angle_radians)
        y_rotated = centre_y + (x - centre_x) * math.sin(angle_radians) + (y - centre_y) * math.cos(angle_radians)
        rotated_coords.append((x_rotated, y_rotated))

    canvas.create_polygon(*sum(rotated_coords, ()), outline="black", fill="lightyellow", width=10, tags="furnishing")

    """Not sure if needed:
    canvas.coords(selected, *rotated_coords)
    canvas.tag_bind("furnishing", "<B1-Motion>", rotate_furnishing)"""


def find_vertices(selected):
    coordinates = canvas.coords(selected)

    return [(coordinates[i], coordinates[i + 1]) for i in range(0, len(coordinates), 2)]


def drag_start(event):
    # record item and its location
    drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y


def drag_stop(event):
    # reset drag information
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0


def drag(event):
    # compute how much mouse has moved
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    # now move the furnishing
    canvas.move(drag_data["item"], delta_x, delta_y)
    # record new pos
    drag_data["x"] = event.x
    drag_data["y"] = event.y


def update_selected(value):
    global buttonSelected
    buttonSelected = value


def button_select(event):
    global buttonSelected
    x = event.x
    y = event.y
    if buttonSelected == 1:
        create_furnishing(1, x, y)
        window.config(cursor="arrow")
    elif buttonSelected == 2:
        create_furnishing(2, x, y)
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

removeEither = tk.Button(master=buttons, text="Pointer", width=10, bg="lightblue",
                         command=lambda: update_selected(0))
removeEither.pack()

message = tk.Label(master=buttons, text="Left click\nto add and\ndrag, right\nclick to\ndelete", width=10, bg="white")
message.pack(pady=10)

# Components to be added to workspace
canvas = tk.Canvas(window, width=500, height=250, bg="lightyellow")
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", button_select)

# used to keep track of a furnishing being dragged
drag_data = {"x": 0, "y": 0, "item": None}

# bound events
canvas.tag_bind("furnishing", "<ButtonPress-3>", delete_furnishing)  # right click
canvas.tag_bind("furnishing", "<ButtonPress-1>", drag_start)  # left click
canvas.tag_bind("furnishing", "<ButtonRelease-1>", drag_stop)  # left click
# canvas.tag_bind("furnishing", "<B1-Motion>", drag)  # left click
# TEST USE
canvas.tag_bind("furnishing", "<B1-Motion>", rotate_furnishing)  # left click

# Build GUI
window.mainloop()
