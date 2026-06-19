from unittest import case

import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Mat3, Vec3, Vec4
from pyglet.gl import *
import random

import shader
from primitives import CustomGroup
from halfedge import Mesh, Halfedge, Vertex, Edge, Face
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

        self.render_mode = ShaderMode.DEFAULT
        self.meshes = []
        self.lights = []
        self.use_base_color_tex = False
        self.use_AO_tex = False
        self.use_specular_tex = False
        self.use_roughness_tex = False
        self.use_normal_mapping = False
        self.modeStr = 'Wireframe Mode'

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        #glClearColor(.3, .3, .3, 1)
        #glLineWidth(2.5)

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
                self.wireframe_batch.draw()
            case ShaderMode.PHONG:
                self.phong_batch.draw()
            case ShaderMode.BLINN_PHONG:
                self.blinn_phong_batch.draw()
            case ShaderMode.GOURAUD:
                self.gouraud_batch.draw()
            case ShaderMode.TEXTURED:
                self.material_batch.draw()
        
        modeText = pyglet.text.Label(self.modeStr, font_size=30, x=10, y=10)
        modeText.draw()
                        

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
                
                shape.transform_mat @= rotate_mat

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
                shape.shader_program["useBaseColor"] = self.use_base_color_tex
                shape.shader_program["useAO"] = self.use_AO_tex
                shape.shader_program["useSpecular"] = self.use_specular_tex
                shape.shader_program["useRoughness"] = self.use_roughness_tex
                shape.shader_program["useNormalMapping"] = self.use_normal_mapping



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
    
    def load_model(self, filename, transform=None, color=None, edge_color=[255, 255, 255, 255], material=None):
        mesh = Mesh(filename.split("/")[-1].split(".")[0])
        
        vertices = []
        normals = []
        indices = []
        vertex_textures = []

        face_colors = []
        vertex_coords = []
        texture_coords = []
        normal_coords = []
        has_vn = False # check if the obj file has vertex normal info
        tangents = []
        
        vertex_texture_map = {}
        edge_halfedges = {}
        wire_indices = []

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
                mesh.vertices.append(Vertex(Vec3(x, y, z), len(mesh.vertices), color))
            if line.startswith("vt "):
                u, v = map(float, line.split()[1:3])
                texture_coords.append((u,v))            
            if line.startswith("vn "):
                if len(line.split()) != 4:
                    print(f"Invalid vertex normal definition: {line}")
                    continue
                x, y, z = map(float, line.split()[1:4])
                normal_coords.append((x, y, z))
                has_vn = True
        
        # read faces and generate halfedge data structure
        for line in lines:
            if line.startswith("f "):
                face_shader_indices = []
                face_obj_indices = []

                vertex_indice = line.split()[1:]
                for vertex_index in vertex_indice:
                    vertex_info = vertex_index.split("/")
                    v_i = int(vertex_info[0]) - 1
                    vt_i = int(vertex_info[1]) - 1 if len(vertex_info) >= 2 and vertex_info[1] else None
                    vn_i = int(vertex_info[2]) - 1 if len(vertex_info) >= 3 and vertex_info[2] else None

                    # accept duplicate vertices with different texture/normal indices
                    v_key = (v_i, vt_i, vn_i)
                    if v_key in vertex_texture_map:
                        shader_i = vertex_texture_map[v_key]
                    else:
                        shader_i = len(vertices) // 3

                        x, y, z = vertex_coords[v_i]
                        u, v = texture_coords[vt_i] if vt_i is not None else (0.0, 0.0)
                        nx, ny, nz = normal_coords[vn_i] if vn_i is not None else (0.0, 0.0, 0.0)
                        
                        vertices.extend([x, y, z])
                        vertex_textures.extend([u, v])
                        normals.extend([nx, ny, nz])
                        tangents.extend([0.0, 0.0, 0.0])

                        vertex_texture_map[v_key] = shader_i

                    face_shader_indices.append(shader_i)
                    face_obj_indices.append(v_i)

                if len(face_shader_indices) < 3:
                    print(f"Invalid face definition: {line}")
                    continue

                # triangulate the face if it has more than 3 vertices
                for j in range(1, len(face_shader_indices) - 1):
                    i0 = face_shader_indices[0]
                    i1 = face_shader_indices[j]
                    i2 = face_shader_indices[j+1]

                    indices.extend([i0,i1,i2])

                    p0 = Vec3(*vertices[i0*3:i0*3+3])
                    p1 = Vec3(*vertices[i1*3:i1*3+3])
                    p2 = Vec3(*vertices[i2*3:i2*3+3])
                    
                    uv0 = vertex_textures[i0*2:i0*2+2]
                    uv1 = vertex_textures[i1*2:i1*2+2]
                    uv2 = vertex_textures[i2*2:i2*2+2]

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

                        for j in [i0, i1, i2]:
                            tangents[j*3+0] += tangent.x
                            tangents[j*3+1] += tangent.y
                            tangents[j*3+2] += tangent.z

                    if not has_vn:
                        # get face normal to calculate area-averaged vertex normals
                        face_normal = (p1 - p0).cross(p2 - p0)

                        for j in [i0,i1,i2]:
                            normals[j*3+0] += face_normal.x
                            normals[j*3+1] += face_normal.y
                            normals[j*3+2] += face_normal.z
                
                # generate halfedges around the face
                face = None
                prev_halfedge = None
                prev_twin_halfedge = None  
                for j in range(len(face_obj_indices)):
                    v_i_start = face_obj_indices[j]
                    v_i_end = face_obj_indices[(j+1)%len(face_obj_indices)]
                    v_start = mesh.vertices[v_i_start]
                    v_end = mesh.vertices[v_i_end]
                    edge = (v_i_start, v_i_end)
                    revesed_edge = (v_i_end, v_i_start)

                    # create halfedge and its twin if the edge is not created
                    if edge not in edge_halfedges:
                        halfedge = Halfedge(v_start)
                        twin_halfedge = Halfedge(v_end)
                        actual_edge = Edge(halfedge)

                        edge_halfedges[edge] = halfedge
                        edge_halfedges[revesed_edge] = twin_halfedge

                        halfedge.edge = actual_edge
                        twin_halfedge.edge = actual_edge
                        halfedge.twin = twin_halfedge
                        twin_halfedge.twin = halfedge

                        mesh.edges.append(actual_edge)
                        mesh.halfedges.append(halfedge)
                        mesh.halfedges.append(twin_halfedge)
                    else:
                        halfedge = edge_halfedges[edge]
                    
                    if v_start.halfedge is None:
                        v_start.halfedge = halfedge
                    if j == 0:
                        face = Face(halfedge)
                        mesh.faces.append(face)
                        start_halfedge = halfedge
                    if j == len(face_shader_indices) - 1:
                        halfedge.next = start_halfedge
                    if prev_halfedge:
                        prev_halfedge.next = halfedge
                    if prev_twin_halfedge and halfedge.twin.next is None:
                        halfedge.twin.next = prev_twin_halfedge
                    prev_halfedge = halfedge
                    prev_twin_halfedge = halfedge.twin
                    halfedge.face = face

        boundary_halfedges = {}
        for edge, halfedge in edge_halfedges.items():
            if halfedge.face is None:
                boundary_halfedges[edge[1]] = halfedge
        
        for v_end, halfedge in boundary_halfedges.items():
            boundary_halfedges[halfedge.vertex.index].next = halfedge

        for j in range(len(normals)//3):
            normal = Vec3(*normals[j*3:j*3+3])
            if normal.length() > 0:
                normal = normal.normalize()
            normals[j*3:j*3+3] = [normal.x, normal.y, normal.z]
        
        for j in range(len(tangents)//3):
            tangent = Vec3(*tangents[j*3:j*3+3])
            if tangent.length() > 0:
                tangent = tangent.normalize()
            tangents[j*3:j*3+3] = [tangent.x, tangent.y, tangent.z]

        wire_set = set()
        for j in range(0, len(indices), 3):
            p0, p1, p2 = indices[j], indices[j+1], indices[j+2]
            for a, b in [(p0, p1), (p1, p2), (p2, p0)]:
                e = tuple(sorted((a, b)))
                if e not in wire_set:
                    wire_set.add(e)
                    wire_indices.extend([a, b])

        self.meshes.append(mesh)
        mesh.print_info()
        #for vertex in mesh.vertices:
            #vertex.print_info()

        if transform is None:
            transform = Mat4.from_translation(self.cam_target)

        if color is None:
            color = [random.randint(40, 250), random.randint(40, 250), random.randint(40, 250), 255]

        face_colors = color * (len(vertices) // 3)
        edge_colors = edge_color * (len(vertices) // 3)

        self.add_faces(transform, vertices, indices, face_colors, normals)
        self.add_wireframes(transform, vertices, wire_indices, edge_colors, normals)
        if material is None:
            material = Material() # set default material
        self.add_faces_with_material(transform, vertices, indices, face_colors, normals, vertex_textures, tangents, material)
        

    def add_faces(self, transform, vertice, indice, color, normal, material=None):
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
        material.bind_textures(shape)
        shape.material = material
        self.shapes.append(shape)

    def add_wireframes(self, transform, vertice, indices, color, normal):
        shape = CustomGroup(transform, len(self.shapes), shader_mode=ShaderMode.DEFAULT)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_LINES, # type: ignore
            batch=self.wireframe_batch,
            group=shape,
            indices=indices,
            vertices=('f', vertice),
            colors=('Bn', color),
            normals = ('f', normal))
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
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    