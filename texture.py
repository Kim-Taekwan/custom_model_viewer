import pyglet
from pyglet.gl import *


class TextureGroup:
    def __init__(self):
        self.textures = {}

    def add_texture(self, name: str, texture: pyglet.image.Texture):
        self.textures[name] = texture
    
    def reset_textures(self):
        self.textures = {}

    def bind_textures(self, shader_program):
        for i, (name, texture) in enumerate(self.textures.items()):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, texture.id)
            shader_program[name] = i