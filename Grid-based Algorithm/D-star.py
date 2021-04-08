import math
import os
import time

import pygame

pygame.init()


# trying to reproduce example in principle of robot motion, appendix H, H.3 D* algorithm

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = float('inf')
        self.k = 0
        self.t = 'new'
        self.parent = None
        self.children = []
        self.isObstacle = False
        self.start = False
        self.goal = False


def ED(current, goal):  # calculate Euclidean Distance
    if not current == goal:
        return math.sqrt((goal.x - current.x) ** 2 + (goal.y - current.y) ** 2)
    else:
        return 0


def Dstar(start, goal):
    openlist = set()

    path = []
    goal.h = 0
    openlist.add(goal)
    goal.t = 'open'
    current = start
    kmin = 0
    while kmin != -1 and current.t != 'close':
        kmin = process_state(openlist)

    path = get_backpointer_list(current, goal)
    return path


def get_backpointer_list(current, goal):
    path = [current]
    while True:
        s = current.parent
        path.append(s)
        if s == goal:
            return path


def insert(openlist, current, h_new):
    if current.t == 'new':
        current.k = h_new
    elif current.t == 'open':
        current.k = min(current.k, h_new)
    elif current.t == 'close':
        current.k = min(current.h, h_new)

    current.h = h_new
    current.t = 'open'
    openlist.add(current)
    return openlist


def cost(node1, node2):
    if node1.isObstacle or node2.isObstacle:
        return float('inf')
    else:
        return ED(node1, node2)


def modify_cost(openlist, node1, node2):
    if node1.t == 'close':
        openlist1 = insert(openlist, node1, node1.h + cost(node1, node2))
    return openlist1


def min_state(openlist):
    if not openlist:
        return -1
    else:
        return min(openlist, key=lambda x: x.k)


def get_kmin(openlist):
    if not openlist:
        return -1
    else:
        return min([x.k for x in openlist])


def delete(x, openlist):
    x.t = 'close'
    openlist.remove(x)
    return openlist


def process_state(open_list):
    x = min_state(open_list)
    if x == -1:
        return -1
    k_old = get_kmin(open_list)
    open_list = delete(x, open_list)
    if k_old < x.h:
        for child in x.children:
            if child.h <= k_old and x.h > child.h + cost(child, x):
                x.parent = child
                x.h = child.h + cost(child, x)
    elif k_old == x.h:
        for child in x.children:
            if child.t == 'new' or (child.parent == x and child.h != x.h + cost(child, x)) \
                    or (child.parent != x and child.h > x.h + cost(child, x)):
                child.parent = x
                open_list = insert(open_list, child, x.h + cost(child, x))
    else:
        for child in x.children:
            if child.t == 'new' or (child.parent == x and child.h != x.h + cost(child, x)):
                child.parent = x
                open_list = insert(open_list, child, x.h + cost(child, x))
            elif (child.parent != x and child.h > x.h + cost(child, x)):
                open_list = insert(open_list, x, x.h)
            elif (child.parent != x and child.h > x.h + cost(child, x)) and (child.t == 'close' and child.h > k_old):
                open_list = insert(open_list, child, child.h)

    return get_kmin(open_list)


def drawRect(color, x, y, screen):
    pygame.draw.rect(screen,
                     color,
                     [(MARGIN + length / GRID_X) * x + MARGIN,
                      (MARGIN + width / GRID_Y) * y + MARGIN,
                      length / GRID_X,
                      width / GRID_Y])


def drawPath(path, color, screen):
    for p in path:
        if not p == S and not p == G:
            drawRect(color, p.x, p.y, screen)
            pygame.display.update()


length = 700
width = 500
GRID_X = 7  # length of grid
GRID_Y = 6  # width of grid
MARGIN = 2  # a parameter related to drawing
os.environ['SDL_VIDEO_CENTERED'] = '1'
# set color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
actualPercentOfWalls = 0  # number of obstacles
# for every grid, create a node class
grid = [[Node(j, i) for i in range(GRID_Y)] for j in range(GRID_X)]

S = grid[1][5]  # set start point
G = grid[GRID_X - 1][0]  # set goal point
# find children for node and set obstacle
obstaclelist = [[1, 0], [2, 0], [1, 1], [2, 1], [1, 2], [2, 2], [1, 3], [2, 3], [3, 4]]
# set obstacle
for x in range(GRID_X):
    for y in range(GRID_Y):
        if [x, y] in obstaclelist:
            grid[x][y].isObstacle = True
            actualPercentOfWalls = actualPercentOfWalls + 1
# find children, obstacle is included
for x in range(GRID_X):
    for y in range(GRID_Y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and j >= 0:
                    if i <= GRID_X - 1 and j <= GRID_Y - 1:
                        if i == x and j == y:
                            continue
                        else:
                            grid[x][y].children.append(grid[i][j])

screen = {}
startTime = time.time()
path = Dstar(S, G)
print("It took %s seconds to run" % (time.time() - startTime))
# drawing
screen = pygame.display.set_mode(
    (length, width), pygame.RESIZABLE)
title = 'D star'
pygame.display.set_caption(title)
for x in range(GRID_X):
    for y in range(GRID_Y):
        if grid[x][y].isObstacle:  # draw obstacle
            drawRect(BLACK, x, y, screen)
        else:  # draw free area
            drawRect(WHITE, x, y, screen)
        if x == S.x and y == S.y:  # draw start point
            drawRect(GREEN, x, y, screen)
        if x == G.x and y == G.y:  # draw goal point
            drawRect(RED, x, y, screen)
pygame.display.flip()  # update surface

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
