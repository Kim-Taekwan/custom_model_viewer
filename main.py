import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from primitives import Cube,Sphere
from control import Control
from material import Material, TextureType


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Local Illumination Model", resizable = True)
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    #free_rock_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.8, 0.8, 0.8), r=6.0)
    #free_rock_material.add_texture("baseColorTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Base_Color.jpg").get_texture(), TextureType.BASE_COLOR)
    #free_rock_material.add_texture("mixedAoTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Mixed_AO.jpg").get_texture(), TextureType.AO)
    #free_rock_material.add_texture("specularTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Specular.jpg").get_texture(), TextureType.SPECULAR)
    #free_rock_material.add_texture("roughnessTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Roughness.jpg").get_texture(), TextureType.ROUGHNESS)
    #free_rock_material.add_texture("normalTex", pyglet.image.load("Free_rock/Free_rock_tex/Free_rock_Normal_OpenGL.jpg").get_texture(), TextureType.NORMAL_MAP)
    #renderer.load_model('Free_rock/Free_rock.obj', color=[250, 190, 190, 255], material=free_rock_material)

    gold_color = [255, 215, 0, 255]
    miku_color = [134, 206, 203, 255]
    renderer.load_model('Miku/MikuTest.obj', color = miku_color, transform = Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)))
    #renderer.load_model('Miku/miku.obj', color = miku_color, transform = Mat4.from_translation(Vec3(-10, -10, 0)) @ Mat4.from_scale(Vec3(10, 10, 10)))

    renderer.add_point_light(position=Vec3(30, 30, 30), intensity=1.0)
    renderer.add_point_light(position=Vec3(-10, 20, 20), intensity=0.3)

    #renderer.add_area_light(width=40, depth=40, interval=5, transform=Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)
    #renderer.add_area_light(40, 40, 5, transform=Mat4.from_rotation(angle=0.785, vector=Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)

    #draw shapes
    renderer.run()
