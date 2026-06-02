import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from primitives import Cube,Sphere
from control import Control


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Rendering & Texturing", resizable = True)
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    #renderer.load_model('model/monkey.obj')
    renderer.load_model('model/miku.obj', color=[134, 206, 203, 255], transform=Mat4.from_translation(Vec3(0, -14, 15)))
    #renderer.load_model('Free_rock/Free_rock.obj', color=[128, 128, 128, 255])

    renderer.add_point_light(position=Vec3(50, 50, 50), intensity=1.0)
    renderer.add_point_light(position=Vec3(-30, 10, 50), intensity=0.3)

    #draw shapes
    renderer.run()
