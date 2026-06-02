import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key
from pyglet.math import Mat4, Vec3, Vec4, Quaternion
import math
from render import RenderWindow
from pyglet.gl import *


class Control:
    """
    Control class controls keyboard & mouse inputs.
    """
    def __init__(self, window: RenderWindow):
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_mouse_motion = self.on_mouse_motion
        window.on_mouse_drag = self.on_mouse_drag
        window.on_mouse_press = self.on_mouse_press
        window.on_mouse_release = self.on_mouse_release
        window.on_mouse_scroll = self.on_mouse_scroll
        self.window = window
        self.setup()

    def setup(self):
        pass

    def update(self, vector):
        pass

    def on_key_press(self, symbol, modifier):
        # move the camera by WASD or arrow keys
        if symbol in [pyglet.window.key.A, pyglet.window.key.LEFT]:
            self.window.move_left = True
        elif symbol in [pyglet.window.key.D, pyglet.window.key.RIGHT]:
            self.window.move_right = True
        elif symbol in [pyglet.window.key.W, pyglet.window.key.UP]:
            self.window.move_forward = True
        elif symbol in [pyglet.window.key.S, pyglet.window.key.DOWN]:
            self.window.move_backward = True
        elif symbol in [pyglet.window.key.E, pyglet.window.key.PAGEUP]:
            self.window.move_up = True
        elif symbol in [pyglet.window.key.Q, pyglet.window.key.PAGEDOWN]:
            self.window.move_down = True
        elif symbol == pyglet.window.key.R:
            self.window.reset_camera()
        elif symbol == pyglet.window.key._1:
            self.window.render_mode = 1
        elif symbol == pyglet.window.key._2:
            self.window.render_mode = 2
        elif symbol == pyglet.window.key._3:
            self.window.render_mode = 3
        elif symbol == pyglet.window.key._4:
            self.window.render_mode = 4
        elif symbol == pyglet.window.key._5:
            self.window.render_mode = 5
        elif symbol in [pyglet.window.key.LSHIFT, pyglet.window.key.RSHIFT]:
            self.window.cam_move_speed = 0.1
        elif symbol == pyglet.window.key.P:
            self.window.save_screenshot()
    
    def on_key_release(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.SPACE:
            self.window.animate = not self.window.animate
        elif symbol == pyglet.window.key.ENTER:
            self.window.spin_light = not self.window.spin_light
        elif symbol in [pyglet.window.key.A, pyglet.window.key.LEFT]:
            self.window.move_left = False
        elif symbol in [pyglet.window.key.D, pyglet.window.key.RIGHT]:
            self.window.move_right = False
        elif symbol in [pyglet.window.key.W, pyglet.window.key.UP]:
            self.window.move_forward = False
        elif symbol in [pyglet.window.key.S, pyglet.window.key.DOWN]:
            self.window.move_backward = False
        elif symbol in [pyglet.window.key.E, pyglet.window.key.PAGEUP]:
            self.window.move_up = False
        elif symbol in [pyglet.window.key.Q, pyglet.window.key.PAGEDOWN]:
            self.window.move_down = False
        elif symbol in [pyglet.window.key.LSHIFT, pyglet.window.key.RSHIFT]:
            self.window.cam_move_speed = 0.05

    def on_mouse_motion(self, x, y, dx, dy):
        # TODO:
        pass

    def on_mouse_press(self, x, y, button, modifier):
        pass

    def on_mouse_release(self, x, y, button, modifier):
        # TODO:
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        # pan the camera by dragging the mouse while pressing the right button
        if button == mouse.LEFT:
            cam_offset = self.window.cam_eye - self.window.cam_target
            radius = cam_offset.length()

            rotate_x = Mat4.from_rotation(-dx * self.window.pan_speed, Vec3(0, 1, 0))
            offset = rotate_x @ Vec4(cam_offset.x, cam_offset.y, cam_offset.z, 0)

            right = cam_offset.cross(self.window.cam_vup).normalize()
            rotate_y = Mat4.from_rotation(-dy * self.window.pan_speed, right)
            offset = rotate_y @ offset

            # limit the pitch to avoid gimbal lock
            max_pitch = math.radians(75.0)
            min_pitch = math.radians(-75.0)
            pitch = math.asin(offset.y / radius)

            if pitch > max_pitch:
                offset = Mat4.from_rotation(max_pitch - pitch, right) @ offset
            elif pitch < min_pitch:
                offset = Mat4.from_rotation(min_pitch - pitch, right) @ offset
            
            self.window.cam_eye = self.window.cam_target + Vec3(offset.x, offset.y, offset.z)
            self.window.update_view_mat()

        #  move the camera by dragging the mouse while pressing the middle button
        if button == mouse.MIDDLE:
            cam_direction = (self.window.cam_target - self.window.cam_eye).normalize()
            right = cam_direction.cross(self.window.cam_vup).normalize()
            up = right.cross(cam_direction).normalize()

            self.window.cam_eye += (-right * dx + -up * dy) * self.window.drag_move_speed
            self.window.cam_target += (-right * dx + -up * dy) * self.window.drag_move_speed
            self.window.update_view_mat()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # zoom in/out by changing cam_eye position
        if scroll_y != 0:
            cam_direction = self.window.cam_target - self.window.cam_eye
            self.window.cam_eye += cam_direction * scroll_y * 0.2
            self.window.update_view_mat()