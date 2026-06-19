import pyglet
from pyglet.gl import *
from enum import Enum
from pyglet.math import Vec3

class TextureType(Enum):
    BASE_COLOR = 1
    AO = 2
    SPECULAR = 3
    ROUGHNESS = 4
    NORMAL_MAP = 5

class Material:
    def __init__(self, ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.8, 0.8, 0.8), r=6.0):
        self.ka = ka
        self.ks = ks
        self.kd = kd
        self.r = r
        
        self.textures = {}
        self.use_base_color_tex = False
        self.use_AO_tex = False
        self.use_specular_tex = False
        self.use_roughness_tex = False
        self.use_normal_map_tex = False

    def add_texture(self, name: str, texture: pyglet.image.Texture,  texture_type: TextureType):
        self.textures[name] = texture
        match texture_type:
            case TextureType.BASE_COLOR:
                self.use_base_color_tex = True
            case TextureType.AO:
                self.use_AO_tex = True
            case TextureType.SPECULAR:
                self.use_specular_tex = True
            case TextureType.ROUGHNESS:
                self.use_roughness_tex = True
            case TextureType.NORMAL_MAP:
                self.use_normal_map_tex = True
                
    
    def reset_textures(self):
        self.textures = {}

    def bind_textures(self, shape):
        for i, (name, texture) in enumerate(self.textures.items()):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(
                GL_TEXTURE_2D,
                GL_TEXTURE_MIN_FILTER,
                GL_LINEAR_MIPMAP_LINEAR
            )
            glTexParameteri(
                GL_TEXTURE_2D,
                GL_TEXTURE_MAG_FILTER,
                GL_LINEAR
            )
            GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE
            glTexParameterf(
                GL_TEXTURE_2D,
                GL_TEXTURE_MAX_ANISOTROPY_EXT,
                16.0
            )
            shape.shader_program[name] = i

        shape.shader_program["useBaseColor"] = self.use_base_color_tex
        shape.shader_program["useAO"] = self.use_AO_tex
        shape.shader_program["useSpecular"] = self.use_specular_tex
        shape.shader_program["useRoughness"] = self.use_roughness_tex
        shape.shader_program["useNormalMapping"] = self.use_normal_map_tex

        shape.shader_program["ka"] = self.ka
        shape.shader_program["kd"] = self.kd
        shape.shader_program["ks"] = self.ks
        shape.shader_program["r"] = self.r