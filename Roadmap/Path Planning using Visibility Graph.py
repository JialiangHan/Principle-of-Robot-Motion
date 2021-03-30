# this file is path planning using visibility graph
# procedure: build visibility graph
#            search using some planning algorithm
import random
from geometry import Node, Polygon, Edge
from Visibility_Map import Visibility_Map
from Computational_Geometry import Convex_hull

# set map size
MAX_X = 50
MAX_Y = 50
MIN_X = 0
MIN_Y = 0

# set start and goal position
start = Node(MIN_X + 1, MIN_Y + 1)
end = Node(MAX_X - 1, MAX_Y - 1)

# random generate polygon, right now rectangular
n = 5  # number of vertex
m = 3  # number of obstacles
node_list = []
edge_list = []
obstacle_list = []
for i in range(m):
    delta_x = (end.x - start.x) / m
    # delta_y = (end.y - start.y) / m
    for j in range(n):
        # random.seed(j)
        x = random.randint(start.x + 1 + i * delta_x, start.x + 1 + (i + 1) * delta_x)
        y = random.randint(start.y + 1, end.y - 1)
        node_list.append(Node(x, y))
    convexhull = Convex_hull(node_list)
    convexhull.run()
    edge_list = []
    for i in range(len(convexhull.hull) - 1):
        edge_list.append(Edge(convexhull.hull[i], convexhull.hull[i + 1]))
    polygon = Polygon(edge_list)
    obstacle_list.append(polygon)
    node_list = []
    edge_list = []

visibility_graph = Visibility_Map(start, end, obstacle_list)
visibility_graph.run()
visibility_graph.plot()
