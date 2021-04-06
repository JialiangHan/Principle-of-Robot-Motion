import numpy as np

import Edge
import Node
import Polygon
import Vertex


def cross_product(list1: list, list2: list) -> int:
    result = list1[0] * list2[1] - list1[1] * list2[0]
    return result


def intersect(edge1: Edge.Edge, edge2: Edge.Edge) -> bool:
    x_max_1 = max(edge1.start.x, edge1.end.x)
    x_min_1 = min(edge1.start.x, edge1.end.x)
    y_max_1 = max(edge1.start.y, edge1.end.y)
    y_min_1 = min(edge1.start.y, edge1.end.y)
    x_max_2 = max(edge2.start.x, edge2.end.x)
    x_min_2 = min(edge2.start.x, edge2.end.x)
    y_max_2 = max(edge2.start.y, edge2.end.y)
    y_min_2 = min(edge2.start.y, edge2.end.y)
    if x_max_2 < x_min_1 or y_max_2 < y_min_1:
        return False
    elif x_max_1 < x_min_2 or y_max_1 < y_min_2:
        return False
    else:
        CA = [edge2.start.x - edge1.start.x, edge2.start.y - edge1.start.y]
        CD = [edge1.end.x - edge1.start.x, edge1.end.y - edge1.start.y]
        CB = [edge2.end.x - edge1.start.x, edge2.end.y - edge1.start.y]
        if cross_product(CA, CD) * cross_product(CB, CD) < 0:
            return True
        else:
            return False


def intersection(edge1: Edge.Edge, edge2: Edge.Edge) -> Node.Node:
    """
    this function return intersection node of two edges
    input type: two edges
    output type: a node
    """
    if intersect(edge1, edge2):
        a = np.array([[edge1.A, edge1.B], [edge2.A, edge2.B]])
        b = np.array([[-edge1.C], [-edge2.C]])
        result = np.linalg.solve(a, b)
        result = Node.Node(result[0], result[1])
        return result


def left_or_right(vertex, edge):
    """
    output is left,right, location of an edge compared to vertex
    """
    result = []
    list_node = [edge.start, edge.end]
    for i in range(len(list_node)):
        if vertex.node == list_node[i]:
            if vertex.node.x > list_node[1 - i].x:
                result.append("left")
            else:
                result.append("right")
    return result


def node_in_edge(node: Node.Node, edge: Edge.Edge) -> list:
    if node == edge.start:
        return [True, edge.end]
    elif node == edge.end:
        return [True, edge.start]
    else:
        return [False, None]


def edge_in_polygon(edge: Edge.Edge, polygon: Polygon.Polygon) -> bool:
    if polygon is None:
        return False
    else:
        if edge in polygon.edge_list:
            return True
        else:
            return False


def node_in_polygon(node: Node.Node, polygon: Polygon.Polygon) -> bool:
    """
    this function determine if a node is inside or on the boundary of a polygon
    :param node:
    :param polygon:
    :return:
    """
    # todo this function has issue, need rewrite
    polygon.vertices.sort(key=lambda x: x.node.x)
    center_edge = Edge.Edge(polygon.vertices[0].node, polygon.vertices[-1].node)
    upper_edge = []
    lower_edge = []
    for edge in polygon.edge_list:
        if not edge.cmp(center_edge):
            if edge.belowOther(center_edge):
                lower_edge.append(edge)
            else:
                upper_edge.append(edge)
    if not upper_edge:
        upper_edge.append(center_edge)
    if not lower_edge:
        lower_edge.append(center_edge)
    for item in lower_edge:
        if item.aboveLine(node):
            temp = 1
        else:
            temp = 0
    for item in upper_edge:
        if not item.aboveLine(node):
            temp = 1
        else:
            temp = 0
    if temp == 1:
        return True
    else:
        return False


def vertex_in_obstacle(vertex: Vertex.Vertex, obstacle_list: list) -> Polygon.Polygon or None:
    """
    this function determine if vertex is in obstacle.vertices
    :param vertex:
    :param obstacle_list:
    :return:
    """
    for obstacle in obstacle_list:
        if vertex in obstacle.vertices:
            return obstacle
    return None
