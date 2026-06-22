from unittest import case

import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Mat3, Vec3, Vec4
from pyglet.gl import *
import random
import os

import shader
from primitives import CustomGroup, Primitive
from shader import ShaderMode
from material import Material, TextureType


class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wireframe_batch = pyglet.graphics.Batch()
        self.default_batch = pyglet.graphics.Batch()
        self.phong_batch = pyglet.graphics.Batch()
        self.blinn_phong_batch = pyglet.graphics.Batch()
        self.gouraud_batch = pyglet.graphics.Batch()        
        self.material_batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.initial_cam_eye = Vec3(0, 10, 20)
        self.initial_cam_target = Vec3(0, 0, 0)
        self.initial_cam_vup = Vec3(0, 1, 0)

        self.cam_eye = self.initial_cam_eye
        self.cam_target = self.initial_cam_target
        self.cam_vup = self.initial_cam_vup
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.01
        self.z_far = 500
        self.fov = 60
        self.proj_mat = None

        self.shapes: list[CustomGroup] = []
        self.setup()

        self.animate = False
        self.move_left = False
        self.move_right = False
        self.move_forward = False
        self.move_backward = False
        self.move_up = False
        self.move_down = False
        self.cam_move_speed = 0.5
        self.cam_dash_speed = 1.0
        self.cam_speed = self.cam_move_speed
        self.drag_move_speed = 0.02
        self.pan_speed = 0.01
        self.cam_rotate_speed = 0.01
        self.spin_light = False

        self.render_mode = ShaderMode.WIREFRAME
        self.meshes = []
        self.lights = []
        self.use_base_color_tex = False
        self.use_AO_tex = False
        self.use_specular_tex = False
        self.use_roughness_tex = False
        self.use_normal_mapping = False
        self.use_toon = True
        self.use_sphere = True
        self.modeStr = 'Wireframe Mode'

        self.wireframe_color = [255, 255, 255, 255]
        self.edge_color = [0, 0, 0, 255]

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(.3, .3, .3, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(2.0)

        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        # 2. Create a projection matrix 
        self.proj_mat = Mat4.perspective_projection(
            aspect = self.width/self.height, 
            z_near=self.z_near, 
            z_far=self.z_far, 
            fov = self.fov)
        
    def update_view_mat(self):
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)

    def on_draw(self) -> None:
        self.clear()
        match self.render_mode:
            case ShaderMode.DEFAULT:
                self.default_batch.draw()
            case ShaderMode.WIREFRAME:
                self.wireframe_batch.draw()
            case ShaderMode.PHONG:
                self.phong_batch.draw()
            case ShaderMode.BLINN_PHONG:
                self.blinn_phong_batch.draw()
            case ShaderMode.GOURAUD:
                self.gouraud_batch.draw()
            case ShaderMode.TEXTURED:
                self.material_batch.draw()
        
        modeText = pyglet.text.Label(self.modeStr, font_size=20, x=10, y=10)
        modeText.draw()

        if self.render_mode == ShaderMode.TEXTURED:
            toon_on_off = "ON" if self.use_toon else "OFF"
            toon_modeText = pyglet.text.Label("Toon: " + toon_on_off, font_size=15, x=10, y=80)
            toon_modeText.draw()
            sphere_on_off = "ON" if self.use_sphere else "OFF"
            sphere_modeText = pyglet.text.Label("Sphere: " + sphere_on_off, font_size=15, x=10, y=50)
            sphere_modeText.draw()
    

    def update(self,dt) -> None:
        view_proj = self.proj_mat @ self.view_mat # type: ignore

        # move the camera by WASD or arrow keys
        cam_direction = (self.cam_target - self.cam_eye).normalize()
        right = cam_direction.cross(self.cam_vup).normalize()
        up = right.cross(cam_direction).normalize()
        if self.move_left:
            self.cam_eye -= (right * self.cam_speed)
            self.cam_target -= (right * self.cam_speed)
            self.update_view_mat()
        if self.move_right:
            self.cam_eye += (right * self.cam_speed)
            self.cam_target += (right * self.cam_speed)
            self.update_view_mat()
        if self.move_forward:
            self.cam_eye += (cam_direction * self.cam_speed)
            self.cam_target += (cam_direction * self.cam_speed)
            self.update_view_mat()
        if self.move_backward:
            self.cam_eye -= (cam_direction * self.cam_speed)
            self.cam_target -= (cam_direction * self.cam_speed)
            self.update_view_mat()
        if self.move_up:
            self.cam_eye += (up * self.cam_speed)
            self.cam_target += (up * self.cam_speed)
            self.update_view_mat()
        if self.move_down:
            self.cam_eye -= (up * self.cam_speed)
            self.cam_target -= (up * self.cam_speed)
            self.update_view_mat()

        if self.spin_light:
            for i, light in enumerate(self.lights):    
                rotate_angle = dt
                rotate_axis = Vec3(0,1,0)
                rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                result = rotate_mat @ Vec4(light["position"].x, light["position"].y, light["position"].z, 1.0)
                light["position"] = result.xyz

        
        for i, shape in enumerate(self.shapes):
            '''
            Update position/orientation in the scene. In the current setting, 
            shapes created later rotate faster while positions are not changed.
            '''
            if self.animate:
                rotate_angle = dt
                rotate_axis = Vec3(0,1,0)
                rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                
                shape.transform_mat = rotate_mat @ shape.transform_mat

                # # Example) You can control the vertices of shape.
                # shape.indexed_vertices_list.vertices[0] += 0.5 * dt

            '''
            Update view and projection matrix. There exist only one view and projection matrix 
            in the program, so we just assign the same matrices for all the shapes
            '''
            shape.shader_program['view_proj'] = view_proj

            if shape.shader_mode in [ShaderMode.GOURAUD, ShaderMode.PHONG, ShaderMode.BLINN_PHONG, ShaderMode.TEXTURED]:
                shape.shader_program["viewPosition"] = self.cam_eye
                shape.shader_program["numLights"] = len(self.lights)
                for i, light in enumerate(self.lights):
                    shape.shader_program[f"lights[{i}].position"] = light["position"]
                    shape.shader_program[f"lights[{i}].color"] = light["color"]
                    shape.shader_program[f"lights[{i}].intensity"] = light["intensity"]
                    shape.shader_program[f"lights[{i}].hasAttenuation"] = light["has_attenuation"]

            if shape.shader_mode == ShaderMode.TEXTURED:
                shape.shader_program["useToon"] = self.use_toon and shape.material.use_toon_tex
                shape.shader_program["useSphere"] = self.use_sphere and shape.material.use_sphere_tex
            #     shape.shader_program["useBaseColor"] = self.use_base_color_tex
            #     shape.shader_program["useAO"] = self.use_AO_tex
            #     shape.shader_program["useSpecular"] = self.use_specular_tex
            #     shape.shader_program["useRoughness"] = self.use_roughness_tex
            #     shape.shader_program["useNormalMapping"] = self.use_normal_mapping


    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED
    
    def reset_camera(self):
        self.cam_eye = self.initial_cam_eye
        self.cam_target = self.initial_cam_target
        self.cam_vup = self.initial_cam_vup
        self.update_view_mat()

    def save_screenshot(self):
        filename = input("Enter filename for screenshot: ")
        screenshot = pyglet.image.get_buffer_manager().get_color_buffer()
        screenshot.save(f"Screenshots/{filename}.png")
        print(f"Screenshot Saved")
    
    def load_model(self, filename, transform=None, color=None, material=None, material_map=None):
        mesh_name = filename.split("/")[-1].split(".")[0]

        if transform is None:
            transform = Mat4.from_translation(self.cam_target)
        
        if color is None:
            color = [random.randint(40, 250), random.randint(40, 250), random.randint(40, 250), 255]

        if material is None:
            material = Material()
        
        vertex_coords = []
        texture_coords = []
        normal_coords = []
        has_vn = False # check if the obj file has vertex normal info
        
        # parse .obj file
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]

        # read vertices
        for line in lines:
            if line.startswith("v "):
                if len(line.split()) != 4:
                    print(f"Invalid vertex definition: {line}")
                    continue
                x, y, z = map(float, line.split()[1:4])
                vertex_coords.append((x, y, z))
            elif line.startswith("vt "):
                u, v = map(float, line.split()[1:3])
                texture_coords.append((u,v))            
            elif line.startswith("vn "):
                if len(line.split()) != 4:
                    print(f"Invalid vertex normal definition: {line}")
                    continue
                x, y, z = map(float, line.split()[1:4])
                normal_coords.append((x, y, z))
                has_vn = True
        
        vertices = []
        indices = []
        normals = []
        tangents = []
        tex_coords = []
        vertex_map = {}

        material_name = mesh_name
        sub_mat = None
        isGrouping = False

        # read faces
        # generate halfedge data structure
        # match material with mesh if those faces are grouped
        for line in lines:
            if line.startswith("usemtl "):
                if isGrouping:
                    self.build_mesh(transform, vertices, indices, normals, tex_coords, tangents, color, edge_color, sub_mat)
                isGrouping = True
                material_name = line.split()[1]
                if material_map is None or material_map.get(material_name) is None:
                    sub_mat = material
                else:
                    sub_mat = material_map.get(material_name)
                vertices = []
                indices = []
                normals = []
                tangents = []
                tex_coords = []
                vertex_map = {}

            elif line.startswith("f "):
                face_indices = []
                face_obj_indices = []
                vertex_indice = line.split()[1:]
                for vertex_index in vertex_indice:
                    vertex_info = vertex_index.split("/")
                    v_i = int(vertex_info[0]) - 1
                    vt_i = int(vertex_info[1]) - 1 if len(vertex_info) >= 2 and vertex_info[1] else None
                    vn_i = int(vertex_info[2]) - 1 if len(vertex_info) >= 3 and vertex_info[2] else None

                    # accept duplicate vertices with different texture/normal indices
                    v_key = (v_i, vt_i, vn_i)
                    if v_key in vertex_map:
                        local_i = vertex_map[v_key]
                    else:
                        local_i = len(vertices) // 3

                        x, y, z = vertex_coords[v_i]
                        u, v = texture_coords[vt_i] if vt_i is not None else (0.0, 0.0)
                        nx, ny, nz = normal_coords[vn_i] if vn_i is not None else (0.0, 0.0, 0.0)
                        
                        vertices.extend([x, y, z])
                        tex_coords.extend([u, v])
                        normals.extend([nx, ny, nz])
                        tangents.extend([0.0, 0.0, 0.0])

                        vertex_map[v_key] = local_i

                    face_indices.append(local_i)
                    face_obj_indices.append(v_i)

                if len(face_indices) < 3:
                    print(f"Invalid face definition: {line}")
                    continue

                # triangulate the face if it has more than 3 vertices
                for j in range(1, len(face_indices) - 1):
                    i0 = face_indices[0]
                    i1 = face_indices[j]
                    i2 = face_indices[j+1]

                    indices.extend([i0, i1, i2])

                    p0 = Vec3(*vertices[i0*3:i0*3+3])
                    p1 = Vec3(*vertices[i1*3:i1*3+3])
                    p2 = Vec3(*vertices[i2*3:i2*3+3])

                    uv0 = tex_coords[i0*2:i0*2+2]
                    uv1 = tex_coords[i1*2:i1*2+2]
                    uv2 = tex_coords[i2*2:i2*2+2]

                    dp1 = p1 - p0
                    dp2 = p2 - p0
                    a = uv1[0] - uv0[0]
                    b = uv2[0] - uv0[0]
                    c = uv1[1] - uv0[1]                    
                    d = uv2[1] - uv0[1]

                    denominator = a * d - b * c
                    if abs(denominator) > 0:
                        tangent = (dp1 * d - dp2 * c) * 1.0 / denominator

                        if tangent.length() > 0:
                            tangent = tangent.normalize()

                        for k in [i0, i1, i2]:
                            tangents[k*3+0] += tangent.x
                            tangents[k*3+1] += tangent.y
                            tangents[k*3+2] += tangent.z

                    if not has_vn:
                        # get face normal to calculate area-averaged vertex normals
                        face_normal = (p1 - p0).cross(p2 - p0)

                        for k in [i0,i1,i2]:
                            normals[k*3+0] += face_normal.x
                            normals[k*3+1] += face_normal.y
                            normals[k*3+2] += face_normal.z
        
        if isGrouping:
            self.build_mesh(transform, vertices, indices, normals, tex_coords, tangents, color, sub_mat)
        else:
            self.build_mesh(transform, vertices, indices, normals, tex_coords, tangents, color, material)


    def build_mesh(self, transform, vertices, indices, normals, tex_coords, tangents, color, material):
        if len(vertices) == 0:
            return

        for i in range(len(normals)//3):
            normal = Vec3(*normals[i*3:i*3+3])
            if normal.length() > 0:
                normal = normal.normalize()
            normals[i*3:i*3+3] = [normal.x, normal.y, normal.z]
        
        for j in range(len(tangents)//3):
            tangent = Vec3(*tangents[j*3:j*3+3])
            if tangent.length() > 0:
                tangent = tangent.normalize()
            tangents[j*3:j*3+3] = [tangent.x, tangent.y, tangent.z]

        wire_indices = []
        wire_set = set()
        for j in range(0, len(indices), 3):
            p0, p1, p2 = indices[j], indices[j+1], indices[j+2]
            for a, b in [(p0, p1), (p1, p2), (p2, p0)]:
                e = tuple(sorted((a, b)))
                if e not in wire_set:
                    wire_set.add(e)
                    wire_indices.extend([a, b])

        face_colors = color * (len(vertices) // 3)

        self.add_faces(transform, vertices, indices, face_colors, normals)
        self.add_edges(transform, vertices, wire_indices)
        self.add_faces_with_material(transform, vertices, indices, face_colors, normals, tex_coords, tangents, material)


    def add_faces(self, transform, vertice, indice, color, normal):
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.DEFAULT)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.default_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        self.shapes.append(shape)

        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.GOURAUD)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.gouraud_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color),
                        normals = ('f', normal))
        self.shapes.append(shape)

        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.PHONG)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.phong_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color),
                        normals = ('f', normal))
        self.shapes.append(shape)

        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.BLINN_PHONG)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.blinn_phong_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color),
                        normals = ('f', normal))
        self.shapes.append(shape)
    
    def add_faces_with_material(self, transform, vertice, indice, color, normal, texture_coords, tangent, material):
        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.TEXTURED)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.material_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color),
                        normals = ('f', normal),
                        tex_coords = ('f', texture_coords),
                        tangents = ('f', tangent)
        )
        material.set_shader_vars(shape)
        shape.material = material
        self.shapes.append(shape)

    def add_edges(self, transform, vertice, indices):
        wireframe_colors = self.wireframe_color * (len(vertice) // 3)
        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.WIREFRAME)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_LINES, # type: ignore
            batch=self.wireframe_batch,
            group=shape,
            indices=indices,
            vertices=('f', vertice),
            colors=('Bn', wireframe_colors))
        self.shapes.append(shape)

        edge_colors = self.edge_color * (len(vertice) // 3)
        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.DEFAULT)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_LINES, # type: ignore
            batch=self.default_batch,
            group=shape,
            indices=indices,
            vertices=('f', vertice),
            colors=('Bn', edge_colors))
        self.shapes.append(shape)

    def add_point_light(self, position, color=Vec3(1.0, 1.0, 1.0), intensity=1.0, has_attenuation=True):
        self.lights.append({
            "position": position,
            "color": color,
            "intensity": intensity,
            "has_attenuation": has_attenuation
        })

    # Area light (implemented as collection of point lights)
    def add_area_light(self, width, depth, interval=5, transform=Mat4.from_translation(Vec3(0, 0, 0)), color=Vec3(1.0, 1.0, 1.0), intensity=0.1, has_attenuation=True):
        for x in range(int(-width/2), int(width/2) + 1, interval):
            for z in range(int(-depth/2), int(depth/2) + 1, interval):
                position = transform @ Vec4(x, 0, z, 1)
                self.add_point_light(Vec3(position.x, position.y, position.z), color, intensity, has_attenuation)

    def add_primitive(self, transform, primitive:Primitive, material=None):
        if material is None:
            material = Material()

        num = len(primitive.vertices) // 3
        texture_coords = [0, 0] * num
        tangents = [0, 0, 0] * num

        wire_indices = []
        wire_set = set()
        for j in range(0, len(primitive.indices), 3):
            p0, p1, p2 = primitive.indices[j], primitive.indices[j+1], primitive.indices[j+2]
            for a, b in [(p0, p1), (p1, p2), (p2, p0)]:
                e = tuple(sorted((a, b)))
                if e not in wire_set:
                    wire_set.add(e)
                    wire_indices.extend([a, b])

        self.add_faces(transform, primitive.vertices, primitive.indices, primitive.colors, primitive.normals)
        self.add_edges(transform, primitive.vertices, wire_indices)
        self.add_faces_with_material(transform, primitive.vertices, primitive.indices, primitive.colors, primitive.normals, texture_coords, tangents, material)
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    