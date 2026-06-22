import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key
from pyglet.math import Mat4, Vec3, Vec4, Quaternion
import math
from render import RenderWindow
from pyglet.gl import *
from shader import ShaderMode


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
        elif symbol == pyglet.window.key._0:
            self.window.modeStr = 'Default Mode'
            self.window.render_mode = ShaderMode.DEFAULT
        elif symbol == pyglet.window.key._1:
            self.window.modeStr = 'Wireframe Mode'
            self.window.render_mode = ShaderMode.WIREFRAME
        elif symbol == pyglet.window.key._2:
            self.window.modeStr = 'Gouraud Illumination Mode'
            self.window.render_mode = ShaderMode.GOURAUD
        elif symbol == pyglet.window.key._3:
            self.window.modeStr = 'Phong Illumination Mode'
            self.window.render_mode = ShaderMode.PHONG
        elif symbol == pyglet.window.key._4:
            self.window.modeStr = 'Blinn-Phong Illumination Mode'
            self.window.render_mode = ShaderMode.BLINN_PHONG
        elif symbol == pyglet.window.key._5:
            self.window.modeStr = 'Texture Mode'
            self.window.render_mode = ShaderMode.TEXTURED
        elif symbol in [pyglet.window.key.LSHIFT, pyglet.window.key.RSHIFT]:
            self.window.cam_speed = self.window.cam_dash_speed
        elif symbol == pyglet.window.key.P:
            self.window.save_screenshot()

        if self.window.render_mode == ShaderMode.TEXTURED:
            if symbol == pyglet.window.key.Z:
                self.window.use_base_color_tex = not self.window.use_base_color_tex
            elif symbol == pyglet.window.key.X:
                self.window.use_AO_tex = not self.window.use_AO_tex
            elif symbol == pyglet.window.key.C:
                self.window.use_specular_tex = not self.window.use_specular_tex
            elif symbol == pyglet.window.key.V:
                self.window.use_roughness_tex = not self.window.use_roughness_tex
            elif symbol == pyglet.window.key.B:
                self.window.use_normal_mapping = not self.window.use_normal_mapping
            elif symbol == pyglet.window.key.T:
                self.window.use_toon = not self.window.use_toon
            elif symbol == pyglet.window.key.Y:
                self.window.use_sphere = not self.window.use_sphere
    
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
            self.window.cam_speed = self.window.cam_move_speed

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
            self.window.cam_eye += cam_direction * scroll_y * 0.1
            self.window.update_view_mat()