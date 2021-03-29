from geometry import Node,Edge,Vertex,Polygon,intersect
from math import atan2,pi
import bisect

def get_vertex_list(node,vertices):
    vertex_list={}
    for vertex in vertices:
        delta_x=vertex.node.x-node.x
        delta_y=vertex.node.y-node.y
        angle=atan2(delta_y,delta_x)
        if angle<0:
            angle=angle+2*pi
        vertex_list[vertex]=angle
        vertex_list1 = sorted(vertex_list.items(), key=lambda x: x[1], reverse=False)
    return vertex_list1

def get_active_list(node, angle, edges):
    active_list = {}
    # set large length
    length = 100000
    x = node.x + length * cos(angle)
    y = node.y + length * sin(angle)
    end = Node(x, y)
    for edge in edges:
        if intersect(edge, Edge(node, end)):
            active_list[edge] = distance_node_to_segment(node, edge)
    active_list = sorted(active_list.items(), key=lambda x: x[1], reverse=False)
    return active_list

def visible(node1,node2,obstacle_list):
    line=Edge(node1,node2)
    for edge in obstacle_list.edge:
        if intersect(line,edge):
            return False
    return True

class Visibility_Map:
    def __init__(self,start,goal, obstacle):
        self.start = start
        self.goal = goal
        self.obstacles = obstacle
        self.vertices = []
        self.get_vertices()
        self.edges = []
        self.visibility_graph = []

    def run(self):
        # this function get all edges for visibility graph
        self.get_graph_edge(self.start, self.vertices)
        self.get_graph_edge(self.end, self.vertices)
        vertices = self.vertices
        for obstacle in self.obstacles:
            self.visibility_graph.append(obstacle.edge)
            vertices.remove(obstacle.vertices)
            for vertex in obstacle.vertices:
                self.get_graph_edge(vertex, vertices)


    def get_graph_edge(self,node,vertices):
                # rotational plane sweep algorithm
        vertex_list = get_vertex_list(node, vertices)  # angle list,sorted
        # sorted edges list that intersect horizontal half-line emanating from node
        edge_list = []
        for vertex in vertices:
            if vertex.edge is not None:
                edge_list.append(vertex.edge)

        active_list = self.get_active_list(node, 0, edge_list)
        for angle in vertex_list:
            if self.visible(node, angle.node, self.obstacles):
                self.visibility_graph.append(Edge(node, angle, node))
            if angle[0].edge_position == "start" and angle[0].edge not in active_list.key:
                active_list[angle[0].edge]=distance_node_to_segment(node, angle[0].edge)




    def get_vertices(self):
        for obstacle in self.obstacles:
            for vertice in obstacle.vertices:
                if vertice not in self.vertices:
                    self.vertices.append(vertice)

    def get_edges(self):
        for obstacle in self.obstacles:
            for edge in obstacle.edge:
                if edge not in self.edges:
                    self.edges.append(edge)
