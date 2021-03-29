# this file is path planning using visibility graph
# procedure: build visibility graph
#            search using some planning algorithm
import random
from geometry import Node, Polygon, Edge
from Visibility_Map import Visibility_Map
from Plot import plot_Edge, plot_Polygon, plot_Node

# set map size
MAX_X = 10
MAX_Y = 10
MIN_X = 0
MIN_Y = 0

# set start and goal position
start = Node(1, 1)
end = Node(9, 9)

# random generate polygon, right now rectangular
n = 4  # number of vertex
node_list = []
edge_list = []
for i in range(n):
    random.seed(i)
    x = random.randint(1, 9)
    y = random.randint(1, 9)
    node_list.append(Node(x, y))
for i in range(len(node_list)):
    if i + 1 < len(node_list):
        edge_list.append(Edge(node_list[i], node_list[i + 1]))
    else:
        edge_list.append(Edge(node_list[-1], node_list[0]))
polygon = Polygon(edge_list)
obstacle_list=[polygon]
visibility_graph = Visibility_Map(start, end, obstacle_list)
visibility_graph.run()

plot_Node(start)
plot_Node(end)
plot_Polygon(polygon)
plot_Edge(visibility_graph.visibility_graph)
