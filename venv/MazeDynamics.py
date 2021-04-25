import pygame
import sys
from tkinter import messagebox, Tk

# constants
size = (width, height) = 640, 480
WALL_COLOUR = (0, 0, 0)
WORLD_COLOUR = (83, 190, 194)  # 18, 166, 136
START_COLOUR = (204, 57, 31)  # 22, 97, 58
END_COLOUR = (214, 21, 82)
PATH_COLOUR = (252, 254, 255)
cols, rows = 64, 48

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Dynamics")

w = width // cols
h = height // rows
grid = []
start_pos = (20, 10)
end_pos = (40, 10)
start_on_hold = False
end_on_hold = False
wallSet = set()
visited = set()
parent = dict()
path = set()
pathActive = False
show_dynamic_message = True


def initialize_path_finder():
    """
    initializes the parent, visited and path
    :return:
    """
    global parent
    global visited
    global path
    path = set()
    visited = set()
    for i in range(cols):
        for j in range(rows):
            parent[(i, j)] = None


def get_neighbors(pos):
    """
    Gets the valid neighbours of the current index.
    :param pos:  current index.
    :return: neighbours list.
    """
    neighbors = []
    x = [-1, 1, 0, 0]
    y = [0, 0, -1, 1]
    for i in range(4):
        a = pos[0] + x[i]
        b = pos[1] + y[i]
        if cols > a >= 0 and rows > b >= 0 and (a, b) not in wallSet and (a, b) not in visited:
            neighbors.append((a, b))
    return neighbors


def get_path():
    """
    Gets the shortest path for the current configuration using breadth first search.
    :return:
    """
    global path
    global start_pos
    q = [start_pos]
    visited.add(start_pos)
    while q:
        current_pos = q.pop(0)
        if current_pos == end_pos:
            break
        valid_neighbours = get_neighbors(current_pos)
        for node in valid_neighbours:
            visited.add(node)
            parent[node] = current_pos
            q.append(node)
    node = end_pos
    while node is not None and node != start_pos:
        path.add(node)
        node = parent[node] if node in parent else None
    if len(path) == 1:
        Tk().wm_withdraw()
        messagebox.showinfo("No Path Found",
                            "No path found for this maze configuration. Press space to reset the maze.")


def draw_world(win, ind):
    """
    Draw the game world on screen
    :param win: window
    :param ind: index
    :return:
    """
    rect = True
    col = WORLD_COLOUR
    if ind in wallSet:
        col = WALL_COLOUR
    elif ind == start_pos:
        col = START_COLOUR
    elif ind == end_pos:
        col = END_COLOUR
    elif ind in path:
        col = PATH_COLOUR
        rect = False
    pygame.draw.rect(win, col, (ind[0] * w, ind[1] * h, w, h)) if rect else pygame.draw.circle(win, col, (
        ind[0] * w + w // 2, ind[1] * h + h // 2), w // 3)


def update_bricks(pos):
    """
    Updates the start and end bricks
    :param pos: position
    :return:
    """
    global start_on_hold
    global end_on_hold
    global pathActive
    if start_on_hold:
        start_on_hold = False
        pathActive = False
    else:
        i = pos[0] // w
        j = pos[1] // h
        if start_pos == (i, j):
            start_on_hold = True
            if pathActive:
                initialize_path_finder()
    if end_on_hold:
        end_on_hold = False
        pathActive = False
    else:
        i = pos[0] // w
        j = pos[1] // h
        if end_pos == (i, j):
            end_on_hold = True
            if pathActive:
                initialize_path_finder()


def reset():
    """
    Resets the screen.
    :return:
    """
    global grid
    global wallSet
    grid = []
    wallSet = set()
    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append((i, j))
        grid.append(arr)


def add_wall(pos):
    """
    Adds the wall
    :param pos: position to add wall
    :return:
    """
    i = pos[0] // w
    j = pos[1] // h
    if (i, j) != start_pos and (i, j) != end_pos:
        wallSet.add((i, j))
        if (i, j) in path:
            if len(path) != 0:
                initialize_path_finder()
            get_path()


def move_start_brick(mouse):
    """
    Move the start brick on the screen
    :param mouse:
    :return:
    """
    global start_pos
    global pathActive
    pos = mouse.get_pos()
    start_pos = (pos[0] // w, pos[1] // h)
    if pathActive:
        if len(path) != 0:
            initialize_path_finder()
        get_path()


def move_end_brick(mouse):
    """
    Moves the end brick
    :param mouse: pygame mouse attribute
    :return:
    """
    global end_pos
    pos = mouse.get_pos()
    end_pos = (pos[0] // w, pos[1] // h)
    if pathActive:
        if len(path) != 0:
            initialize_path_finder()
        get_path()


reset()
# game loop
flag = 0


def clear_wall(pos):
    """
    Clear the wall in the position pos
    :param pos: position to clear wall
    :return:
    """
    i = pos[0] // w
    j = pos[1] // h
    if (i, j) in wallSet:
        wallSet.remove((i, j))
        if pathActive:
            if len(path) != 0:
                initialize_path_finder()
            get_path()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # check if the mouse click is on start brick or end brick and handle the event
                update_bricks(pygame.mouse.get_pos())
                # add walls
                add_wall(pygame.mouse.get_pos())
            if event.button == 3:
                clear_wall(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEMOTION:
            if start_on_hold:
                move_start_brick(pygame.mouse)
            if end_on_hold:
                move_end_brick(pygame.mouse)
            if event.buttons[0]:
                add_wall(pygame.mouse.get_pos())
            if event.buttons[2]:
                clear_wall(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # if space key pressed, resets the screen.
                reset()
                initialize_path_finder()
            if event.key == pygame.K_RETURN:
                # if enter key pressed, find the path from start brick to end brick.
                initialize_path_finder()
                get_path()
                if len(path) > 1:
                    pathActive = True
    # updates the screen.
    for i in range(cols):
        for j in range(rows):
            draw_world(screen, (i, j))
    pygame.display.update()
    if flag == 0:
        Tk().wm_withdraw()
        messagebox.showinfo("Maze Dynamics",
                            "Move the bricks, draw walls, press enter to find path, press space to reset."
                            " Have fun!")
        flag = 1
