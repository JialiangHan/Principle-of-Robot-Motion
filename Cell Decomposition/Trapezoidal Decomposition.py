"""
this file is a trapezoidal decomposition of a map
"""
from geometry import intersection, Polygon, Node, Edge, left_or_right,edge_in_polygon,vertex_in_obstacle
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
        obstacle = vertex_in_obstacle(current_vertex, self.obstacle)
        for i in range(len(current_vertex.edge_list)):
            # position[edge]= left or right
            position[current_vertex.edge_list[i]] = left_or_right(current_vertex, current_vertex.edge_list[i])
        # determine if upper or lower
        if current_vertex.edge_list[0].start != current_vertex.node:
            if current_vertex.edge_list[1].start != current_vertex.node:
                if current_vertex.edge_list[0].start.y > current_vertex.edge_list[1].start.y:
                    E_upper = current_vertex.edge_list[0]
                    E_lower = current_vertex.edge_list[1]
                else:
                    E_upper = current_vertex.edge_list[1]
                    E_lower = current_vertex.edge_list[0]
            else:
                if current_vertex.edge_list[0].start.y > current_vertex.edge_list[1].end.y:
                    E_upper = current_vertex.edge_list[0]
                    E_lower = current_vertex.edge_list[1]
                else:
                    E_upper = current_vertex.edge_list[1]
                    E_lower = current_vertex.edge_list[0]
        else:
            if current_vertex.edge_list[1].start != current_vertex.node:
                if current_vertex.edge_list[0].end.y > current_vertex.edge_list[1].start.y:
                    E_upper = current_vertex.edge_list[0]
                    E_lower = current_vertex.edge_list[1]
                else:
                    E_upper = current_vertex.edge_list[1]
                    E_lower = current_vertex.edge_list[0]
            else:
                if current_vertex.edge_list[0].end.y > current_vertex.edge_list[1].end.y:
                    E_upper = current_vertex.edge_list[0]
                    E_lower = current_vertex.edge_list[1]
                else:
                    E_upper = current_vertex.edge_list[1]
                    E_lower = current_vertex.edge_list[0]

        if position[E_upper][0] == "right" and position[E_lower][0] == "right":
            # insert E_upper and E_lower into current_edge
            self.current_edge_list.insert(E_upper, E_upper)
            self.current_edge_list.insert(E_lower, E_lower)
            prev = self.getPred(E_lower)
            succ = self.getSucc(E_upper)
        elif position[E_upper][0] == "right" and position[E_lower][0] == "left":
            # delete E_lower and insert E_upper
            prev = self.getPred(E_lower)
            self.current_edge_list.remove(E_lower)
            self.current_edge_list.insert(E_upper, E_upper)
            succ = self.getSucc(E_upper)
        elif position[E_upper][0] == "left" and position[E_lower][0] == "right":
            # delete E_upper and insert E_lower
            succ = self.getSucc(E_upper)
            self.current_edge_list.remove(E_upper)
            self.current_edge_list.insert(E_lower, E_lower)
            prev = self.getPred(E_lower)
        else:
            # delete E_upper and E_lower
            succ = self.getSucc(E_upper)
            prev = self.getPred(E_lower)
            self.current_edge_list.remove(E_upper)
            self.current_edge_list.remove(E_lower)
        if prev is not None:
            if not edge_in_polygon(prev, obstacle):
                inter1 = intersection(prev, sweepline)
                self.vertical_extension.append(Edge(current_vertex.node, inter1))
        if succ is not None:
            if not edge_in_polygon(succ, obstacle):
                inter2 = intersection(succ, sweepline)
                self.vertical_extension.append(Edge(current_vertex.node, inter2))

    def getPred(self, edge: Edge):
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
m = 2  # number of obstacles
delta_x = (MAX_X - MIN_X) / m
delta_y = (MAX_Y - MIN_Y) / m
node_list = []
edge_list = []
obstacle_list = []
for i in range(m):
    for j in range(n):
        random.seed(j)
        x = random.uniform(MIN_X + 1 + i * delta_x, MIN_X + 1 + (i + 1) * delta_x)
        y = random.uniform(MIN_Y + 10, MAX_Y - 20)
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
node_list = [Node(1, 30), Node(10, 0), Node(40, 2), Node(55, 40), Node(30, 50),Node(5,45)]
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
# plt.show()
trapezoidal_decomposition = Trapezoidal_Decomposition(boundary, obstacle_list)
trapezoidal_decomposition.run()
trapezoidal_decomposition.plot()
