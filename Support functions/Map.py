"""
this file contains a map class which contains some obstacle
"""
import random
from Computational_Geometry import Convex_hull
from geometry import Polygon,Edge,Node
import matplotlib.pyplot as plt
from Plot import plot_Edge,plot_Polygon


class Map:
    def __init__(self,size:list,n:int):
        """
        size:list, a list which show max range of map,[min_x,max_x,min_y,max_y]
        n: number of obstacle
        """
        self.min_x=size[0]
        self.max_x=size[1]
        self.min_y=size[2]
        self.max_y=size[3]
        self.number_of_obstacle=n
        self.obstacle_list=[]
        self.generate_obstacle()
        self.boundary_edge=[]
        self.generate_boundary()

    def generate_boundary(self):
        left_lower=Node(self.min_x,self.min_y)
        left_upper=Node(self.min_x,self.max_y)
        right_upper=Node(self.max_x,self.max_y)
        right_lower=Node(self.max_x,self.min_y)
        left_edge=Edge(left_lower,left_upper)
        ri

    def generate_obstacle(self):
        number_of_nodes = 5  # number of vertex
        node_list = []
        edge_list = []
        delta_x = (self.max_x - self.min_x) / self.number_of_obstacle
        for i in range(self.number_of_obstacle):
            for j in range(number_of_nodes):
                # random.seed(j)
                x = random.uniform(self.max_x + 1 + i * delta_x, self.min_x + 1 + (i + 1) * delta_x)
                y = random.uniform(self.min_y + 1, self.max_y - 1)
                node_list.append(Node(x, y))
            convexhull = Convex_hull(node_list)
            convexhull.run()
            for i in range(len(convexhull.hull) - 1):
                edge_list.append(Edge(convexhull.hull[i], convexhull.hull[i + 1]))
            polygon = Polygon(edge_list)
            self.obstacle_list.append(polygon)
            node_list = []
            edge_list = []

    def Plot(self):
        plot_Edge()
        for obstacle in self.obstacle_list:
            plot_Polygon(obstacle)