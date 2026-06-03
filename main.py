import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from primitives import Cube,Sphere
from control import Control
from texture import TextureGroup


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Rendering & Texturing", resizable = True)
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    #renderer.load_model('model/miku.obj', color=[134, 206, 203, 255], transform=Mat4.from_translation(Vec3(0, -14, 15)))

    free_rock_textures = TextureGroup()
    free_rock_textures.add_texture("baseColorTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Base_Color.jpg").get_texture())
    free_rock_textures.add_texture("mixedAoTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Mixed_AO.jpg").get_texture())
    free_rock_textures.add_texture("specularTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Specular.jpg").get_texture())
    free_rock_textures.add_texture("roughnessTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Roughness.jpg").get_texture())
    #free_rock_textures.add_texture("normalTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Normal_OpenGL.jpg").get_texture())
    renderer.load_model('Free_rock/Free_rock.obj', color=[190, 190, 190, 255], texture_group=free_rock_textures)

    renderer.add_point_light(position=Vec3(50, 50, 50), intensity=1.0)
    renderer.add_point_light(position=Vec3(-30, 10, 50), intensity=0.3)

    #draw shapes
    renderer.run()
