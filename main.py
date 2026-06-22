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

    free_rock_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.8, 0.8, 0.8), r=6.0)
    free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Base_Color.jpg", TextureType.BASE_COLOR)
    free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Mixed_AO.jpg", TextureType.AO)
    free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Specular.jpg", TextureType.SPECULAR)
    free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Roughness.jpg", TextureType.ROUGHNESS)
    free_rock_material.add_texture("Free_rock/Free_rock_tex/Free_rock_Normal_OpenGL.jpg", TextureType.NORMAL_MAP)
    renderer.load_model('Free_rock/Free_rock.obj', color=[190, 190, 190, 255], material=free_rock_material)

    gold_color = [255, 215, 0, 255]
    miku_color = [134, 206, 203, 255]
    skin_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.6, 0.6, 0.6), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    clothes_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    clothes2_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    panel_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    glow_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    pantsu_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    headset_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    headset2_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    hair_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    hair_shadow_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=10.0)
    face_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.8, 0.8, 0.8), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    oral_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.8, 0.8, 0.8), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    eyes_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=5.0)
    expression_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=5.0)
    _01_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.5, 0.5, 0.5), r=6.0)
    outline_mat = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.039, 0.235, 0.255), ks=Vec3(0.3, 0.3, 0.3), r=5.0)
    
    skin_mat.add_texture("Miku/Tex_Miku/Miku_Skin.png", TextureType.BASE_COLOR)
    skin_mat.add_texture("Miku/Tex_Miku/Toon_Skin.png", TextureType.TOON)
    skin_mat.add_texture("Miku/Tex_Miku/Sph_Skin.png", TextureType.SPHERE)
    clothes_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)
    clothes_mat.add_texture("Miku/Tex_Miku/Toon_Clothes.png", TextureType.TOON)
    clothes_mat.add_texture("Miku/Tex_Miku/Sph_Clothes.png", TextureType.SPHERE)
    clothes2_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)
    clothes2_mat.add_texture("Miku/Tex_Miku/Toon_Clothes.png", TextureType.TOON)
    clothes2_mat.add_texture("Miku/Tex_Miku/Sph_Clothes2.png", TextureType.SPHERE)
    panel_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)
    panel_mat.add_texture("Miku/Tex_Miku/Sph_Panel.png", TextureType.SPHERE)
    glow_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)
    hair_mat.add_texture("Miku/Tex_Miku/Miku_Hair.png", TextureType.BASE_COLOR)
    hair_mat.add_texture("Miku/Tex_Miku/Toon_Hair.png", TextureType.TOON)
    hair_mat.add_texture("Miku/Tex_Miku/Sph_Hair.png", TextureType.SPHERE)
    hair_shadow_mat.add_texture("Miku/Tex_Miku/Miku_Hair.png", TextureType.BASE_COLOR)
    headset_mat.add_texture("Miku/Tex_Miku/Miku_Headset.png", TextureType.BASE_COLOR)
    headset_mat.add_texture("Miku/Tex_Miku/Sph_Headset.png", TextureType.SPHERE)
    headset2_mat.add_texture("Miku/Tex_Miku/Miku_Headset.png", TextureType.BASE_COLOR)
    pantsu_mat.add_texture("Miku/Tex_Miku/Miku_pantsu.png", TextureType.BASE_COLOR)
    pantsu_mat.add_texture("Miku/Tex_Miku/Toon_Clothes.png", TextureType.TOON)
    pantsu_mat.add_texture("Miku/Tex_Miku/Sph_Skin.png", TextureType.SPHERE)
    face_mat.add_texture("Miku/Tex_Miku/Miku_Face.png", TextureType.BASE_COLOR)
    face_mat.add_texture("Miku/Tex_Miku/Toon_Skin.png", TextureType.TOON)
    oral_mat.add_texture("Miku/Tex_Miku/Miku_Face.png", TextureType.BASE_COLOR)
    eyes_mat.add_texture("Miku/Tex_Miku/Miku_Eyes.png", TextureType.BASE_COLOR)
    expression_mat.add_texture("Miku/Tex_Miku/Miku_Expression.png", TextureType.BASE_COLOR)
    _01_mat.add_texture("Miku/Tex_Miku/Miku_Clothes.png", TextureType.BASE_COLOR)

    miku_material_map = {
        "Skin": skin_mat,
        "Clothes": clothes_mat,
        "Clothes2": clothes2_mat,
        "Glow": glow_mat,
        "Skirt": clothes2_mat,
        "Panel": panel_mat,
        "Tie": clothes2_mat,
        "gizagiza": clothes_mat,
        "01": _01_mat,
        "Pantsu": pantsu_mat,
        "Headset": headset_mat,
        "Headset2": headset2_mat,
        "Hair": hair_mat,
        "Hair_Shadow": hair_shadow_mat,
        "Hair_Transparent1": hair_mat,
        "Hair_Transparent2": hair_mat,
        "Oral": oral_mat,
        "Face": face_mat,
        "Eyes": eyes_mat,
        "Expression": expression_mat,
        "Expression2": expression_mat,
        "Outline": outline_mat
    }
    miku_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.6, 0.6, 0.6), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    #renderer.load_model('Miku/MikuTest.obj', color=gold_color, transform=Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)), material=miku_material, material_map=miku_material_map)
    #renderer.load_model('Miku/miku.obj', color = gold_color, transform = Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 3)), material=miku_material, material_map=miku_material_map)

    renderer.add_point_light(position=Vec3(100, 80, 100), intensity=1.0, has_attenuation=False)
    #renderer.add_point_light(position=Vec3(30, 30, 30), intensity=0.8)
    #renderer.add_point_light(position=Vec3(-10, 20, 20), intensity=0.2)
    #renderer.add_point_light(position=Vec3(-10, -20, 20), intensity=0.1)

    #renderer.add_area_light(width=40, depth=40, interval=5, transform=Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)
    #renderer.add_area_light(40, 40, 5, transform=Mat4.from_rotation(angle=0.785, vector=Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)

    #draw shapes
    renderer.run()
