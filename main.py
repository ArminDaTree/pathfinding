from tkinter import *

nb_case = 10
window_side = 600
cote_case = window_side // nb_case
fenetre = Tk()
fenetre.title("Pathfinding")
canvas = Canvas(fenetre, width=window_side, height=window_side, background='white')
points = [(-1, -1), (-1, -1)]
Grid = [[0 for col in range(nb_case)] for row in range(nb_case)]

def reset_Grid():
    for x in range(nb_case):
        for y in range(nb_case):
            Grid[x][y] = 0

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def dist(node_pos, end_pos):
    return ((node_pos[0] - end_pos[0]) ** 2) + ((node_pos[1] - end_pos[1]) ** 2)


def pathfinding(grid, start, end):
    # init start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    # init open and closed list
    open_list = [start_node]
    closed_list = []

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:  # end
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        #for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares (with diagonal)
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: #without diagonals
            node_pos = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_pos[0] > nb_case-1 or node_pos[0] < 0 or node_pos[1] > nb_case-1 or node_pos[1] < 0:
                continue  # prochain tour de boucle
            if grid[node_pos[0]][node_pos[1]] != 0:  # obstacle
                continue
            new_node = Node(current_node, node_pos)
            children.append(new_node)
        for child in children:
            if child in closed_list:
                continue
            child.g = current_node.g + 1
            #child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.h = dist(child.position, end_node.position)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)

def drawpath(path):
    if path is not None:
        for coord in path[1:len(path)-1]:
            x = coord[0]*cote_case
            y = coord[1]*cote_case
            canvas.create_rectangle(x, y, x + cote_case, y + cote_case, fill="khaki1")
    else:
        print("pas de chemins !!")


def left_click(event):
    x = event.x // cote_case
    y = event.y // cote_case
    if points[0] != (-1, -1):
        previous_x = points[0][0] * cote_case
        previous_y = points[0][1] * cote_case
        canvas.create_rectangle(previous_x, previous_y, previous_x + cote_case, previous_y + cote_case, fill="white")
    points[0] = (x, y)
    canvas.create_rectangle(x * cote_case, y * cote_case, x * cote_case + cote_case, y * cote_case + cote_case, fill="spring green")


def right_click(event):
    x = event.x // cote_case
    y = event.y // cote_case
    if points[1] != (-1, -1):
        previous_x = points[1][0] * cote_case
        previous_y = points[1][1] * cote_case
        canvas.create_rectangle(previous_x, previous_y, previous_x + cote_case, previous_y + cote_case, fill="white")
    points[1] = (x, y)
    canvas.create_rectangle(x * cote_case, y * cote_case, x * cote_case + cote_case, y * cote_case + cote_case,fill="green2")


def middle_click(event):
    x = (event.x // cote_case)
    y = (event.y // cote_case)
    if Grid[x][y] == 1:
        Grid[x][y] = 0
        canvas.create_rectangle(x*cote_case, y*cote_case, x*cote_case + cote_case, y*cote_case + cote_case, fill="white")
    else:
        Grid[x][y] = 1
        canvas.create_rectangle(x*cote_case, y*cote_case, x*cote_case + cote_case, y*cote_case + cote_case, fill="grey")

def createGrid(canvas):
    reset_Grid()
    canvas.delete("all")
    for i in range(1, nb_case):
        canvas.create_line(cote_case * i, 0, cote_case * i, window_side)
        canvas.create_line(0, cote_case * i, window_side, cote_case * i)
    canvas.pack()


def key_handler(event):
    if event.keysym == "t":
        if points[0] != (-1, -1) and points[1] != (-1, -1):
            path = pathfinding(Grid, points[0], points[1])
            drawpath(path)
    if event.keysym == "Return":
        print("Reset !")
        createGrid(canvas)


if __name__ == '__main__':
    createGrid(canvas)
    canvas.bind("<Button-1>", left_click)
    canvas.bind("<Button-2>", middle_click)
    canvas.bind("<Button-3>", right_click)
    fenetre.bind("<Key>", key_handler)
    fenetre.mainloop()
