import pyglet
from pyglet import window, app, shapes
from pyglet.math import Mat4, Vec3, Vec4
import math
from pyglet.gl import *

import shader

class CustomGroup(pyglet.graphics.Group):
    '''
    To draw multiple 3D shapes in Pyglet, you should make a group for an object.
    '''
    def __init__(self, transform_mat: Mat4, order, shader_mode = shader.ShaderMode.DEFAULT):
        super().__init__(order)

        '''
        Create shader program for each shape
        '''
        self.material = None
        
        self.shader_mode = shader_mode
        if shader_mode == shader.ShaderMode.DEFAULT:
            self.shader_program = shader.create_program(
                shader.vertex_source_default, shader.fragment_source_default
            )
        if shader_mode == shader.ShaderMode.WIREFRAME:
            self.shader_program = shader.create_program(
                shader.vertex_source_default, shader.fragment_source_default
            )
        elif shader_mode == shader.ShaderMode.GOURAUD:
            self.shader_program = shader.create_program(
                shader.vertex_source_gouraud, shader.fragment_source_gouraud
            )
        elif shader_mode == shader.ShaderMode.PHONG:
            self.shader_program = shader.create_program(
                shader.vertex_source_phong, shader.fragment_source_phong
            )
        elif shader_mode == shader.ShaderMode.BLINN_PHONG:
            self.shader_program = shader.create_program(
                shader.vertex_source_blinn_phong, shader.fragment_source_blinn_phong
            )
        elif shader_mode == shader.ShaderMode.TEXTURED:
            self.shader_program = shader.create_program(
                shader.vertex_source_material, shader.fragment_source_material
            )

        self.transform_mat = transform_mat
        self.indexed_vertices_list = None
        self.shader_program.use()

    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model
        if self.material is not None:
            self.material.bind_textures(self)

    def unset_state(self):
        self.shader_program.stop()

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent)
    
    def __hash__(self):
        return hash((self.order)) 
    
class Primitive:
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.colors = ()
        self.normals = []

# Reconstructed to define normals correctly
class Cube(Primitive):
    '''
    default structure of cube
    '''
    def __init__(self, scale=Vec3(x=1.0, y=1.0, z=1.0), color=Vec4(255, 255, 255, 255)):
        super().__init__()
        
        
        sx, sy, sz = scale.x, scale.y, scale.z

        self.vertices = [
            -0.5, -0.5,  0.5,
             0.5, -0.5,  0.5,
             0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5,
            -0.5,  0.5, -0.5,
             0.5,  0.5, -0.5,
             0.5, -0.5, -0.5,

            -0.5, -0.5, -0.5,
            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,

             0.5, -0.5,  0.5,
             0.5, -0.5, -0.5,
             0.5,  0.5, -0.5,
             0.5,  0.5,  0.5,

            -0.5,  0.5,  0.5,
             0.5,  0.5,  0.5,
             0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,

            -0.5, -0.5, -0.5,
             0.5, -0.5, -0.5,
             0.5, -0.5,  0.5,
            -0.5, -0.5,  0.5,
        ]
        self.vertices = [scale[idx%3] * x for idx, x in enumerate(self.vertices)]

        self.normals = [
            0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,
            0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1,
            -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,
            1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,
            0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,
            0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0,
        ]

        self.indices = [
            0, 1, 2,  2, 3, 0,
            4, 5, 6,  6, 7, 4,
            8, 9,10, 10,11, 8,
           12,13,14, 14,15,12,
           16,17,18, 18,19,16,
           20,21,22, 22,23,20,
        ]

        self.colors = (color[0], color[1], color[2], color[3]) * 24
        
class Sphere(Primitive):
    '''
    default structure of sphere
    '''
    def __init__(self, stacks, slices, scale=1.0, color=Vec4(255, 255, 255, 255)):
        super().__init__()
        num_triangles = 2 * slices * (stacks - 1)

        for i in range(stacks):
            phi0 = 0.5 * math.pi - (i * math.pi) / stacks
            phi1 = 0.5 * math.pi - ((i + 1) * math.pi) / stacks
            coord_v0 = 1.0 - float(i) / stacks
            coord_v1 = 1.0 - float(i + 1) / stacks

            y0 = scale * math.sin(phi0)
            r0 = scale * math.cos(phi0)
            y1 = scale * math.sin(phi1)
            r1 = scale * math.cos(phi1)
            y2 = y1
            y3 = y0

            for j in range(slices):
                theta0 = (j * 2 * math.pi) / slices
                theta1 = ((j + 1) * 2 * math.pi) / slices
                coord_u0 = float(j) / slices
                coord_u1 = float(j + 1) / slices

                x0 = r0 * math.cos(theta0)
                z0 = r0 * math.sin(-theta0)
                u0 = coord_u0
                v0 = coord_v0
                x1 = r1 * math.cos(theta0)
                z1 = r1 * math.sin(-theta0)
                u1 = coord_u0
                v1 = coord_v1
                x2 = r1 * math.cos(theta1)
                z2 = r1 * math.sin(-theta1)
                u2 = coord_u1
                v2 = coord_v1
                x3 = r0 * math.cos(theta1)
                z3 = r0 * math.sin(-theta1)
                u3 = coord_u1
                v3 = coord_v0

                n0 = Vec3(x0, y0, z0).normalize()
                n1 = Vec3(x1, y1, z1).normalize()
                n2 = Vec3(x2, y2, z2).normalize()
                n3 = Vec3(x3, y3, z3).normalize()

                if (i != stacks - 1):
                    self.vertices.extend([x0, y0, z0])
                    self.vertices.extend([x1, y1, z1])
                    self.vertices.extend([x2, y2, z2])

                    self.normals.extend([n0.x, n0.y, n0.z])
                    self.normals.extend([n1.x, n1.y, n1.z])
                    self.normals.extend([n2.x, n2.y, n2.z])
                    
                    self.colors += (color[0], color[1], color[2], color[3])
                    self.colors += (color[0], color[1], color[2], color[3])
                    self.colors += (color[0], color[1], color[2], color[3])
                
                if (i != 0):
                    self.vertices.extend([x2, y2, z2])
                    self.vertices.extend([x3, y3, z3])
                    self.vertices.extend([x0, y0, z0])
                    
                    self.normals.extend([n2.x, n2.y, n2.z])
                    self.normals.extend([n3.x, n3.y, n3.z])
                    self.normals.extend([n0.x, n0.y, n0.z])
                    
                    self.colors += (color[0], color[1], color[2], color[3])
                    self.colors += (color[0], color[1], color[2], color[3])
                    self.colors += (color[0], color[1], color[2], color[3])

        for i in range(num_triangles*3):
            self.indices.append(i)