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

def visible(node1,node2,obstacle_list):
    line=Edge(node1,node2)
    for edge in obstacle_list.edge:
        if intersect(line,edge):
            return False
    return True

class Visibility_Map:
    def __init__(self,start,goal, obstacle):
        self.start=start
        self.goal=goal
        self.obstacles=obstacle
        self.vertices=[]
        self.edges=[]
        self.visibility_graph=[]

    def run(self):


    def get_graph_edge(self,node,vertices):
        #rotational plane sweep algorithm
        vertex_list=get_vertex_list(node,vertices) # angle list,sorted
        # sorted edges list that intersect horizontal half-line emanating from node
        active_list=self.get_active_list(node,vertices)
        for angle in vertex_list:
            if self.visible(node,angle.node,self.obstacles):
                self.visibility_graph.append(Edge(node,angle,node))
            if angle[0].edge_position=="start" and angle[0].edge not in active_list:
                active_list.append(angle[0].edge)




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
