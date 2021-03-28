# this file contains all distance functions:
# distance between nodes
# distance from node to segment
# distance from node to polygon
from math import sqrt


def dist(a, b):
    # a, b are nodes from geometry
    delta_x = a.x - b.x
    delta_y = a.y - b.y
    distance = sqrt(delta_y ^ 2 + delta_x ^ 2)
    return distance

def dist_node_line(node,segment):
    