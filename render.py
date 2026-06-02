from unittest import case

import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3, Vec4
from pyglet.gl import *
import random

import shader
from primitives import CustomGroup
from halfedge import Mesh, Halfedge, Vertex, Edge, Face



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.point_batch = pyglet.graphics.Batch()
        self.edge_batch = pyglet.graphics.Batch()
        self.face_batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(0,0,25)
        self.cam_target = Vec3(0,0,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.01
        self.z_far = 100
        self.fov = 60
        self.proj_mat = None

        self.shapes = []
        self.setup()

        self.animate = False
        self.move_left = False
        self.move_right = False
        self.move_forward = False
        self.move_backward = False
        self.move_up = False
        self.move_down = False
        self.cam_move_speed = 0.05
        self.drag_move_speed = 0.01
        self.pan_speed = 0.01
        self.cam_rotate_speed = 0.01

        self.render_mode = 1 # 1: wireframe, 2: phong, 3: texture, 4: normal mapping

        self.meshes = []
        self.vertex_selected = None

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        #glClearColor(.3, .3, .3, 1)
        glLineWidth(2.5)

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
            case 1: self.edge_batch.draw() # wireframe mode
            case 2: self.face_batch.draw() # phong shading mode
            case 3: pass # texture mode
            case 4: pass # normal mapping mode
            case _: pass
        

    def update(self,dt) -> None:
        view_proj = self.proj_mat @ self.view_mat # type: ignore

        # move the camera by WASD or arrow keys
        cam_direction = (self.cam_target - self.cam_eye).normalize()
        right = cam_direction.cross(self.cam_vup).normalize()
        up = right.cross(cam_direction).normalize()
        if self.move_left:
            self.cam_eye -= (right * self.cam_move_speed)
            self.cam_target -= (right * self.cam_move_speed)
            self.update_view_mat()
        if self.move_right:
            self.cam_eye += (right * self.cam_move_speed)
            self.cam_target += (right * self.cam_move_speed)
            self.update_view_mat()
        if self.move_forward:
            self.cam_eye += (cam_direction * self.cam_move_speed)
            self.cam_target += (cam_direction * self.cam_move_speed)
            self.update_view_mat()
        if self.move_backward:
            self.cam_eye -= (cam_direction * self.cam_move_speed)
            self.cam_target -= (cam_direction * self.cam_move_speed)
            self.update_view_mat()
        if self.move_up:
            self.cam_eye += (up * self.cam_move_speed)
            self.cam_target += (up * self.cam_move_speed)
            self.update_view_mat()
        if self.move_down:
            self.cam_eye -= (up * self.cam_move_speed)
            self.cam_target -= (up * self.cam_move_speed)
            self.update_view_mat()
        
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

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED
    
    def load_model(self, filename, transform=None, face_color=None, point_color=[255, 255, 0, 255], edge_color=[255, 255, 255, 255]):
        mesh = Mesh(filename.split("/")[-1].split(".")[0])
        vertice = []
        indice = []
        face_colors = []
        edge_halfedges = {}
        edge_indice = []

        # parse .obj file
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                # vertex
                if line.startswith("v "):
                    if len(line.split()) != 4:
                        print(f"Invalid vertex definition: {line}")
                        continue
                    x, y, z = map(float, line.split()[1:4])
                    vertice.extend([x, y, z])
                    mesh.vertices.append(Vertex(Vec3(x, y, z), len(mesh.vertices), point_color))

                # face
                elif line.startswith("f "):
                    # get only vertex index (ignore texture and normal indices)
                    face_v_i = []
                    vertex_indice = line.split()[1:]
                    for vertex_index in vertex_indice:
                        v_i = int(vertex_index.split("/")[0]) - 1
                        face_v_i.append(v_i)
                    if len(face_v_i) < 3:
                        print(f"Invalid face definition: {line}")
                        continue

                    # triangulate the face if it has more than 3 vertices
                    for i in range(1, len(face_v_i) - 1):
                        indice.extend([face_v_i[0], face_v_i[i], face_v_i[i + 1]])
                    
                    # generate halfedges around the face
                    face = None
                    prev_halfedge = None
                    prev_twin_halfedge = None  
                    for i in range(len(face_v_i)):
                        v_i_start = face_v_i[i]
                        v_i_end = face_v_i[(i+1)%len(face_v_i)]
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
                        if i == 0:
                            face = Face(halfedge)
                            mesh.faces.append(face)
                            start_halfedge = halfedge
                        if i == len(face_v_i) - 1:
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
            edge_indice.extend(edge)
            if halfedge.face is None:
                boundary_halfedges[edge[1]] = halfedge
        
        for v_end, halfedge in boundary_halfedges.items():
            boundary_halfedges[halfedge.vertex.index].next = halfedge

        self.meshes.append(mesh)
        mesh.print_info()
        #for vertex in mesh.vertices:
            #vertex.print_info()


        if transform is None:
            transform = Mat4.from_translation(self.cam_target)

        if face_color is None:
            face_color = [random.randint(40, 250), random.randint(40, 250), random.randint(40, 250), 255]

        face_colors = face_color * (len(vertice) // 3)
        edge_colors = edge_color * (len(vertice) // 3)

        self.add_faces(transform, vertice, indice, face_colors)
        self.add_edges(transform, vertice, edge_indice, edge_colors)
        

    def add_faces(self, transform, vertice, indice, color):
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES, # type: ignore
                        batch = self.face_batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        self.shapes.append(shape)

    def add_edges(self, transform, vertices, indices, color):
        shape = CustomGroup(transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertices)//3, GL_LINES, # type: ignore
            batch=self.edge_batch,
            group=shape,
            indices=indices,
            vertices=('f', vertices),
            colors=('Bn', color)
        )
        self.shapes.append(shape)
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    