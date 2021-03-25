from geometry import Node,Edge,Vertice,Polygon
def get_vertex_list(node,vertices):
    vertex_list={}
    for vertex in vertices:
        vertex_list
    return vertex_list

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
            if self.visible(node,angle.node):
                self.visibility_graph.append(Edge(node,angle,node))




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
