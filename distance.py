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


def distance_node_to_segment(node, segment):
    # distance between node and segment
    slope_start, intercept_start = perpendicular(segment.start, segment)
    slope_end, intercept_end = perpendicular(segment.end, segment)
    if line_value(slope_start, intercept_start, node) * line_value(slope_end, intercept_end, node) < 0:
        distance = abs(line_value(segment.slope, segment.intercept, node) / sqrt(segment.slope ^ 2 + 1))
    else:
        distance = min(dist(node, segment.start), dist(node, segment.end))
    return distance


def line_value(slope, intercept, node):
    result = slope * node.x + intercept - node.y
    return result


def perpendicular(node, segment):
    # this function return a line that perpendicular to segment and pass the node
    slope = -1 / segment.slope
    intercept = node.y - slope * node.x
    return slope, intercept
