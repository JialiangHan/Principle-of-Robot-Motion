"""
this file is a trapezoidal decomposition of a map
"""
from geometry import intersection, Polygon, Node, Edge
import heapq
import random
from Plot import plot_Edge, plot_Polygon
import matplotlib.pyplot as plt


class Trapezoidal_Decomposition:
    def __init__(self, boundary, obstacle):
        self.boundary = boundary
        self.obstacle = obstacle
        self.vertices = []
        self.get_vertices()
        self.edge_list = []
        self.vertical_extension = []

    def run(self):
        current_vertex = heapq.heappop(self.vertices)

    def plot(self):
        for edge in self.vertical_extension:
            plot_Edge(edge)
        plt.show()

    def get_vertices(self):
        for vertex in self.boundary.vertices:
            heapq.heappush(self.vertices, vertex)
        for obstacle in self.obstacle:
            for vertex in obstacle.vertices:
                heapq.heappush(self.vertices, vertex)


# set map size
MAX_X = 50
MAX_Y = 50
MIN_X = 0
MIN_Y = 0

# random generate polygon
n = 3  # number of vertex
m = 3  # number of obstacles
delta_x = (MAX_X - MIN_X) / m
delta_y = (MAX_Y - MIN_Y) / m
node_list = []
edge_list = []
obstacle_list = []
for i in range(m):
    for j in range(n):
        # random.seed(j)
        x = random.uniform(MIN_X + 1 + i * delta_x, MIN_X + 1 + (i + 1) * delta_x)
        y = random.uniform(MIN_Y + 1, MAX_Y - 1)
        node_list.append(Node(x, y))
    for k in range(len(node_list)):
        if k + 1 < len(node_list):
            edge_list.append(Edge(node_list[k], node_list[k + 1]))
        else:
            edge_list.append(Edge(node_list[k], node_list[0]))
    polygon = Polygon(edge_list)
    obstacle_list.append(polygon)
    node_list = []
    edge_list = []
# generate boundary
delta1 = delta_x
delta2 = 1
node_list = [Node(1, -1), Node(48, 0), Node(51, 5), Node(52, 45), Node(43, 51), Node(5, 50), Node(-1, 40), Node(-2, 10)]
for k in range(len(node_list)):
    if k + 1 < len(node_list):
        edge_list.append(Edge(node_list[k], node_list[k + 1]))
    else:
        edge_list.append(Edge(node_list[k], node_list[0]))
boundary = Polygon(edge_list)

fig1 = plt.figure()
for edge in boundary.edge:
    plot_Edge(edge)
for obstacle in obstacle_list:
    plot_Polygon(obstacle)

trapezoidal_decomposition = Trapezoidal_Decomposition(boundary, obstacle_list)
trapezoidal_decomposition.run()
trapezoidal_decomposition.plot()
