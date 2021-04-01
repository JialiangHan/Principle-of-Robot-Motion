"""
this file is a trapezoidal decomposition of a map
"""
from geometry import intersection, Polygon, Node, Edge, determine_edge_location
import heapq
import random
from Plot import plot_Edge, plot_Polygon
import matplotlib.pyplot as plt
from bintrees import AVLTree


class Trapezoidal_Decomposition:
    def __init__(self, boundary, obstacle):
        self.boundary = boundary
        self.obstacle = obstacle
        self.vertices = []
        self.get_vertices()
        self.current_edge_list = AVLTree()
        self.vertical_extension = []

    def run(self):
        while self.vertices:
            current_vertex = heapq.heappop(self.vertices)
            self.process_event(current_vertex)

    def process_event(self, current_vertex):
        """
        this function determine event type for current_vertex
        and maintain current edge list
        """
        position = {}
        # end node is a selected node far away on sweep line
        end_up_node = Node(current_vertex.node.x, 1000)
        end_down_node = Node(current_vertex.node.x, -1000)
        sweepline = Edge(end_up_node, end_down_node)
        for edge in current_vertex.edge_list:
            position[edge] = determine_edge_location(current_vertex, edge)
            if position[edge][1] == "upper":
                E_upper = edge
            else:
                E_lower = edge
        # Todo AVL tree is somehow is empty, need to fix
        if position[E_upper] == "right" and position[E_lower] == "right":
            # insert E_upper and E_lower into current_edge
            self.current_edge_list.insert(E_upper)
            self.current_edge_list.insert(E_lower)
            prev = self.getPred(E_lower)
            succ=self.getSucc(E_upper)
            inter1 = intersection(prev, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter1))
            inter2 = intersection(succ, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter2))
        elif position[E_upper] == "right" and position[E_lower] == "left":
            # delete E_lower and insert E_upper
            prev = self.getPred(E_lower)
            self.current_edge_list.remove(E_lower)
            self.current_edge_list.insert(E_upper)
            succ=self.getSucc(E_upper)
            inter1 = intersection(prev, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter1))
            inter2 = intersection(succ, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter2))
        elif position[E_upper] == "left" and position[E_lower] == "right":
            # delete E_upper and insert E_lower
            succ=self.getSucc(E_upper)
            self.current_edge_list.remove(E_upper)
            self.current_edge_list.insert(E_lower)
            prev = self.getPred(E_lower)
            inter1 = intersection(prev, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter1))
            inter2 = intersection(succ, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter2))
        else:
            # delete E_upper and E_lower
            succ=self.getSucc(E_upper)
            prev = self.getPred(E_lower)
            self.current_edge_list.remove(E_upper)
            self.current_edge_list.remove(E_lower)
            inter1 = intersection(prev, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter1))
            inter2 = intersection(succ, sweepline)
            self.vertical_extension.append(Edge(current_vertex.node, inter2))

    def getPred(self, edge:Edge):
        try:
            return self.current_edge_list.prev_key(edge)
        except KeyError:
            return None

    def getSucc(self, edge: Edge):
        try:
            return self.current_edge_list.succ_key(edge)
        except KeyError:
            return None

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
