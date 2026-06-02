import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from primitives import Cube,Sphere
from control import Control


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "3D Model with  and textures", resizable = True)
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    #renderer.load_model('model/monkey.obj', transform=Mat4.from_translation(vector=Vec3(x=-4, y=1, z=0)))
    #renderer.load_model('model/miku.obj', face_color=[134, 206, 203, 255])
    #renderer.load_model('model/monkey.obj', transform=Mat4.from_translation(vector=Vec3(x=-4, y=1, z=0)))
    renderer.load_model('Free_rock/Free_rock.obj', point_color=[128, 128, 128, 255])

    #renderer.add_point_light(Vec3(0, 5, 5), Vec3(1, 1, 1))

    #draw shapes
    renderer.run()
