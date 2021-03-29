from geometry import Node, Edge, Vertex, Polygon, intersect
from distance import distance_node_to_segment
from math import atan2, pi, cos, sin


class Visibility_Map:
    def __init__(self, start, goal, obstacle):
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
        self.get_graph_edge(self.goal, self.vertices)
        vertices = self.vertices
        for obstacle in self.obstacles:
            self.visibility_graph.append(obstacle.edge)
            vertices.remove(obstacle.vertices)
            for vertex in obstacle.vertices:
                self.get_graph_edge(vertex, vertices)

    def get_graph_edge(self, node, vertices):
        # rotational plane sweep algorithm
        vertex_list = self.get_vertex_list(node, vertices)  # angle list,sorted
        # sorted edges list that intersect horizontal half-line emanating from node
        edge_list = []  # edge list of vertices, should be all edges of obstacle
        for vertex in vertices:
            if vertex.edge is not None:
                edge_list.append(vertex.edge)
        active_list = self.get_active_list(node, pi/4, edge_list)
        for item in vertex_list:
            angle=item[1]
            vertex=item[0]
            if self.visible(node, vertex.node, self.obstacles):
                self.visibility_graph.append(Edge(node, angle, vertex))
            if vertex.edge_position == "start" and vertex.edge not in active_list.key:
                active_list[vertex.edge] = distance_node_to_segment(node, vertex.edge)
                active_list = sorted(active_list.items(), key=lambda x: x[1], reverse=False)
            if vertex.edge_position == "end" and vertex.edge in active_list.key:
                active_list.pop(vertex.edge)

    def get_vertices(self):
        for obstacle in self.obstacles:
            for vertex in obstacle.vertices:
                if vertex not in self.vertices:
                    self.vertices.append(vertex)

    def get_edges(self):
        for obstacle in self.obstacles:
            for edge in obstacle.edge:
                if edge not in self.edges:
                    self.edges.append(edge)

    def get_vertex_list(self,node, vertices):
        # this function return angle between node and vertices
        vertex_list = {}
        for vertex in vertices:
            delta_x = vertex.node.x - node.x
            delta_y = vertex.node.y - node.y
            angle = atan2(delta_y, delta_x)
            if angle < 0:
                angle = angle + 2 * pi
            vertex_list[vertex] = angle
        vertex_list1 = sorted(vertex_list.items(), key=lambda x: x[1], reverse=False)
        return vertex_list1

    @staticmethod
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

    @staticmethod
    def visible(node1, node2, obstacle_list):
        # check if node1 and node2 are visible regarding to obstacle
        line = Edge(node1, node2)
        for obstacle in obstacle_list:
            for edge in obstacle.edge:
                if intersect(line, edge):
                    return False
        return True