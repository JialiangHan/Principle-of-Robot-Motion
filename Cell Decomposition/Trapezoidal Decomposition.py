"""
this file is a trapezoidal decomposition of a map
"""
from geometry import intersection
import heapq


class Trapezoidal_Decom():
    def __init__(self, boundary, obstacle):
        self.boundary = boundary
        self.obstacle = obstacle
        self.vertices=[]
        self.get_vertices
        self.edge_list=[]

    def get_vertices(self):
        for vertex in self.boundary.vertices:
            heapq.heappush(self.vertices,vertex)
        for vertex in self.obstacle.vertices:
            heapq.heappush(self.vertices,vertex)