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

    # free_rock_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.8, 0.8, 0.8), r=6.0)
    # free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Base_Color.jpg", TextureType.BASE_COLOR)
    # free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Mixed_AO.jpg", TextureType.AO)
    # free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Specular.jpg", TextureType.SPECULAR)
    # free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Roughness.jpg", TextureType.ROUGHNESS)
    # free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Normal_OpenGL.jpg", TextureType.NORMAL_MAP)
    # renderer.load_model('Free_rock/Free_rock.obj', color=[190, 190, 190, 255], material=free_rock_material)

    gold_color = [255, 215, 0, 255]
    miku_color = [134, 206, 203, 255]
    skin_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.6, 0.6, 0.6), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    clothes_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    pantsu_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    headset_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    hair_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    face_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.8, 0.8, 0.8), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    eyes_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=5.0)
    expression_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=5.0)
    outline_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.039, 0.235, 0.255), ks=Vec3(0.3, 0.3, 0.3), r=5.0)
    
    skin_mat.add_texture("Miku/Tex_Miku/Miku_Skin.png", TextureType.BASE_COLOR)
    clothes_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)
    pantsu_mat.add_texture("Miku/Tex_Miku/Miku_pantsu.png", TextureType.BASE_COLOR)
    headset_mat.add_texture("Miku/Tex_Miku/Miku_Headset.png", TextureType.BASE_COLOR)
    hair_mat.add_texture("Miku/Tex_Miku/Miku_Hair.png", TextureType.BASE_COLOR)
    face_mat.add_texture("Miku/Tex_Miku/Miku_Face.png", TextureType.BASE_COLOR)
    eyes_mat.add_texture("Miku/Tex_Miku/Miku_Eyes.png", TextureType.BASE_COLOR)
    expression_mat.add_texture("Miku/Tex_Miku/Miku_Expression.png", TextureType.BASE_COLOR)

    miku_material_map = {
        "Skin": skin_mat,
        "Clothes": clothes_mat,
        "Clothes2": clothes_mat,
        "Glow": clothes_mat,
        "Skirt": clothes_mat,
        "Panel": clothes_mat,
        "Tie": clothes_mat,
        "gizagiza": clothes_mat,
        "01": clothes_mat,
        "Pantsu": pantsu_mat,
        "Headset": headset_mat,
        "Headset2": headset_mat,
        "Hair": hair_mat,
        "Hair_Shadow": hair_mat,
        "Hair_Transparent1": hair_mat,
        "Hair_Transparent2": hair_mat,
        "Oral": face_mat,
        "Face": face_mat,
        "Eyes": eyes_mat,
        "Expression": expression_mat,
        "Expression2": expression_mat,
        "Outline": outline_mat
    }
    miku_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.6, 0.6, 0.6), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    renderer.load_model('Miku/MikuTest.obj', color=gold_color, transform=Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)),
                        material=miku_material, material_map=miku_material_map)
    #renderer.load_model('Miku/miku.obj', color = miku_color, transform = Mat4.from_translation(Vec3(-10, -10, 0)) @ Mat4.from_scale(Vec3(10, 10, 10)))

    #renderer.add_point_light(position=Vec3(100, 100, 100), intensity=1.0, has_attenuation=False)
    renderer.add_point_light(position=Vec3(30, 30, 30), intensity=1.0)
    renderer.add_point_light(position=Vec3(-10, 20, 20), intensity=0.3)

    #renderer.add_area_light(width=40, depth=40, interval=5, transform=Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)
    #renderer.add_area_light(40, 40, 5, transform=Mat4.from_rotation(angle=0.785, vector=Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)

    #draw shapes
    renderer.run()
