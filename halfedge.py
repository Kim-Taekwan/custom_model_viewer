import pyglet
from pyglet import window, app, shapes
from pyglet.math import Mat4, Vec3, Vec4
import math
from pyglet.gl import *

class Mesh:
    def __init__(self, name):
        self.name = name
        self.halfedges = []
        self.vertices = []
        self.edges = []
        self.faces = []
        self.colors = []

    def print_info(self):
        print(f"Mesh: {self.name}")
        print(f"# of vertices: {len(self.vertices)}")
        print(f"# of edges: {len(self.edges)}")
        print(f"# of faces: {len(self.faces)}")
        #print(f"# of halfedges: {len(self.halfedges)}")

class Halfedge:
    def __init__(self, vertex):
        self.vertex = vertex
        self.edge = None
        self.face = None
        self.next = None
        self.twin = None

class Vertex:
    def __init__(self, position: Vec3, index: int, color=None):
        self.position = position
        self.index = index
        self.color = color
        self.halfedge = None

    def num_neighbors(self):
        count = 0
        cur_halfedge = self.halfedge
        while True:
            count += 1
            cur_halfedge = cur_halfedge.twin.next
            if cur_halfedge == self.halfedge:
                break
        return count
    
    def print_info(self):
        print(f"Vertex {self.index}: position={self.position}, num_neighbors={self.num_neighbors()}")

class Edge:
    def __init__(self, halfedge: Halfedge):
        self.halfedge = halfedge

class Face:
    def __init__(self, halfedge: Halfedge):
        self.halfedge = halfedge
    
    def num_vertices(self):
        count = 0
        cur_halfedge = self.halfedge
        while True:
            count += 1
            cur_halfedge = cur_halfedge.next
            if cur_halfedge == self.halfedge:
                break
        return count