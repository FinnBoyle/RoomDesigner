import math
import tkinter as tk

buttonSelected = 0


def follow_cursor(event):
    global spot
    spot.destroy()
    spot = tk.Label(text=f"{round(event.x / 100, 1)}, {round(event.y / 100, 1)}")
    spot.place(x=event.x+100, y=event.y+25)


def delete_furnishing(event):
    canvas.delete(canvas.find_closest(event.x, event.y))


def rotate(event, clockwise):
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

    rotated_coords = []
    for x, y in coordinates:
        x_rotated = centre_x + (x - centre_x) * math.cos(amount) - (y - centre_y) * math.sin(amount)
        y_rotated = centre_y + (x - centre_x) * math.sin(amount) + (y - centre_y) * math.cos(amount)
        rotated_coords.append((round(x_rotated, 5), round(y_rotated, 5)))

    canvas.delete(selected)

    # if rotated_coords == 2, then shape is a line, if rotated_coords == 4, it is a rectangle
    if len(rotated_coords) == 2:
        canvas.create_line(*sum(rotated_coords, ()), fill="red", width=10)
    elif len(rotated_coords) == 4:
        canvas.create_polygon(*sum(rotated_coords, ()), outline="black", fill="lightyellow", width=5)


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


def create_start(event):
    # capture initial coordinates for polygon (top left corner)
    resize_drag_data["start_x"] = event.x
    resize_drag_data["start_y"] = event.y


def create_stop(event, button):
    # Use final values to calculate polygon size
    x1 = resize_drag_data["start_x"]
    y1 = resize_drag_data["start_y"]
    x2 = resize_drag_data["end_x"]
    y2 = resize_drag_data["end_y"]
    if button == 1:
        canvas.create_line(x1, y1, x2, y2, fill="red", width=10)
    elif button == 2:
        vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
        canvas.create_polygon(vertices, outline="black", fill="lightyellow", width=5)

        resize_drag_data["start_x"] = 0
        resize_drag_data["start_y"] = 0
        resize_drag_data["end_x"] = 0
        resize_drag_data["end_y"] = 0
    else:
        pass


def create_size(event):
    # capture final polygon coordinates (bottom right corner)  as the mouse is moved
    resize_drag_data["end_x"] = event.x
    resize_drag_data["end_y"] = event.y


def update_selected(value):
    global buttonSelected
    buttonSelected = value


def button_select(event):
    global buttonSelected
    x = event.x
    y = event.y
    if buttonSelected == 1:
        window.config(cursor="arrow")
    elif buttonSelected == 2:
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


def escape(event):
    window.attributes("-fullscreen", False)

# Create window
window = tk.Tk()
window.title("Room Designer")
window.minsize(1000, 500)
window.attributes("-fullscreen", True)

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

reset = tk.Button(master=buttons, text="Pointer", width=10, bg="lightblue", command=lambda: update_selected(0))
reset.pack()

message = tk.Label(master=buttons, text="Left click\nand drag to\ndraw shape.\nRight click\nand drag\nto move\nshape",
                   width=10)
message.pack(pady=5)

message2 = tk.Label(master=buttons, text="Right/left\narrow keys to\nrotate items\nclockwise/\nanticlockwise")
message2.pack()

message3 = tk.Label(master=buttons, text="Press\nBackspace\nto delete.", width=10)
message3.pack(pady=5)

message4 = tk.Label(master=buttons, text="Press\nEscape to\nleave\nfullscreen.", width=10)
message4.pack()

spot = tk.Label(text="")  # to be updated
spot.place(x=0, y=0)

# Components to be added to workspace
canvas = tk.Canvas(window, width=500, height=250, bg="lightyellow")
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Button-1>", button_select)

# used to keep track of a furnishing being dragged
move_drag_data = {"x": 0, "y": 0, "item": None}
resize_drag_data = {"start_x": 0, "start_y": 0, "end_x": 0, "end_y": 0}

# bound events
canvas.focus_set()
# BackSpace
canvas.bind("<BackSpace>", delete_furnishing)
# right click
canvas.bind("<ButtonPress-3>", drag_start)
canvas.bind("<ButtonRelease-3>", drag_stop)
canvas.bind("<B3-Motion>", drag)
# left click
canvas.bind("<ButtonPress-1>", create_start)
canvas.bind("<ButtonRelease-1>", lambda event: create_stop(event, buttonSelected))
canvas.bind("<B1-Motion>", lambda event: (create_size(event), follow_cursor(event)))
# arrow keys
canvas.bind("<Left>", lambda event: rotate(event, False))
canvas.bind("<Right>", lambda event: rotate(event, True))
# Escape key
canvas.bind("<Escape>", escape)

canvas.bind("<Motion>", follow_cursor)
# Build GUI
window.mainloop()
