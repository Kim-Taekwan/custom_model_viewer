import pyglet
from pyglet import window, app, shapes
from pyglet.math import Mat4, Vec3, Vec4
import math
from pyglet.gl import *

import shader

class CustomGroup(pyglet.graphics.Group):
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
        elif shader_mode == shader.ShaderMode.TOON_EDGE:
            self.shader_program = shader.create_program(
                shader.vertex_source_edge, shader.fragment_source_edge
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
