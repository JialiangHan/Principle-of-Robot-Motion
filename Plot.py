# this file is a collection for plot functions
# include plot_node, plot_edge, plot_polygon
import matplotlib.pyplot as plt


def plot_Node(node):
    plt.plot(node.x, node.y, ".k")


def plot_Edge(edge):
    plt.plot([edge.start.x, edge.end.x], [edge.start.y, edge.end.y], "k")


def plot_Polygon(polygon):
    x, y = [], []
    for vertex in polygon.vertices:
        x.append(vertex.x)
        y.append(vertex.y)
    plt.fill(x, y, "b")
