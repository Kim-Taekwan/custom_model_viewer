import pyglet
from pyglet.math import Mat4, Vec3, Vec4

from render import RenderWindow
from control import Control
from material import Material, TextureType

def render_genoge_miku():
    #gold_color = [255, 215, 0, 255]
    miku_color = [134, 206, 203, 255]
    skin_mat = Material(kd=Vec3(0.95, 0.95, 0.95), ks=Vec3(0.03, 0.03, 0.03))
    clothes_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    clothes2_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    tie_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    panel_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    glow_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    pantsu_mat = Material(ks=Vec3(0.1, 0.1, 0.1))
    headset_mat = Material(ks=Vec3(0.2, 0.2, 0.2), r=6.0)
    headset2_mat = Material(ks=Vec3(0.2, 0.2, 0.2), r=6.0)
    hair_mat = Material(ks=Vec3(0.1, 0.1, 0.1))
    hair_shadow_mat = Material(ks=Vec3(0.1, 0.1, 0.1))
    face_mat = Material(kd=Vec3(0.95, 0.95, 0.95), ks=Vec3(0.03, 0.03, 0.03))
    oral_mat = Material(ks=Vec3(0.25, 0.25, 0.25))
    eyes_mat = Material(kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.3, 0.3, 0.3), r=2.0)
    expression_mat = Material(kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.3, 0.3, 0.3), r=4.0)
    _01_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    outline_mat = Material(ka=Vec3(0.0, 0.0, 0.0), kd=Vec3(0.039, 0.235, 0.255))

    white_tex = "textures/white_tex.png"
    tex_path = "Miku/Genoge/Tex_Miku"
    skin_mat.add_texture("Miku_Skin.png", TextureType.BASE_COLOR, tex_path)
    skin_mat.add_texture("Toon_Skin.png", TextureType.TOON, tex_path)
    skin_mat.add_texture("Sph_Skin.png", TextureType.SPHERE, tex_path)
    skin_mat.enable_toon_edge(toon_edge_color=Vec4(0.612, 0.306, 0.306, 1.0), toon_edge_size=.0005)

    clothes_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    clothes_mat.add_texture("Toon_Clothes.png", TextureType.TOON, tex_path)
    clothes_mat.add_texture("Sph_Clothes.png", TextureType.SPHERE, tex_path)
    clothes_mat.enable_toon_edge(toon_edge_color=Vec4(0.231, 0.231, 0.231, 1.0), toon_edge_size=.0005)

    clothes2_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    clothes2_mat.add_texture("Toon_Clothes.png", TextureType.TOON, tex_path)
    clothes2_mat.add_texture("Sph_Clothes2.png", TextureType.SPHERE, tex_path)
    clothes2_mat.enable_toon_edge(toon_edge_color=Vec4(0.0, 0.0, 0.0, 1.0), toon_edge_size=.0005)

    tie_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    tie_mat.add_texture("Toon_Clothes.png", TextureType.TOON, tex_path)
    tie_mat.add_texture("Sph_Clothes2.png", TextureType.SPHERE, tex_path)
    tie_mat.enable_toon_edge(toon_edge_color=Vec4(0.231, 0.231, 0.231, 1.0), toon_edge_size=.0005)

    face_mat.add_texture("Miku_Face.png", TextureType.BASE_COLOR, tex_path)
    face_mat.add_texture("Toon_Skin.png", TextureType.TOON, tex_path)
    #face_mat.enable_toon_edge(toon_edge_color=Vec4(0.667, 0.325, 0.325, 1.0), toon_edge_size=.0003)

    panel_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    panel_mat.add_texture(white_tex, TextureType.TOON)
    panel_mat.add_texture("Sph_Panel.png", TextureType.SPHERE, tex_path)

    glow_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    glow_mat.add_texture(white_tex, TextureType.TOON)

    hair_mat.add_texture("Miku_Hair.png", TextureType.BASE_COLOR, tex_path)
    hair_mat.add_texture("Toon_Hair.png", TextureType.TOON, tex_path)
    hair_mat.add_texture("Sph_Hair.png", TextureType.SPHERE, tex_path)

    hair_shadow_mat.add_texture("Miku_Hair.png", TextureType.BASE_COLOR, tex_path)
    hair_shadow_mat.add_texture(white_tex, TextureType.TOON)

    headset_mat.add_texture("Miku_Headset.png", TextureType.BASE_COLOR, tex_path)
    headset_mat.add_texture(white_tex, TextureType.TOON)
    headset_mat.add_texture("Sph_Headset.png", TextureType.SPHERE, tex_path)

    headset2_mat.add_texture("Miku_Headset.png", TextureType.BASE_COLOR, tex_path)
    headset2_mat.add_texture(white_tex, TextureType.TOON)

    pantsu_mat.add_texture("Miku_pantsu.png", TextureType.BASE_COLOR, tex_path)
    pantsu_mat.add_texture("Toon_Clothes.png", TextureType.TOON, tex_path)
    pantsu_mat.add_texture("Sph_Skin.png", TextureType.SPHERE, tex_path)

    oral_mat.add_texture("Miku_Face.png", TextureType.BASE_COLOR, tex_path)
    oral_mat.add_texture(white_tex, TextureType.TOON)

    eyes_mat.add_texture("Miku_Eyes.png", TextureType.BASE_COLOR, tex_path)
    eyes_mat.add_texture(white_tex, TextureType.TOON)

    expression_mat.add_texture("Miku_Expression.png", TextureType.BASE_COLOR, tex_path)
    expression_mat.add_texture(white_tex, TextureType.TOON)

    _01_mat.add_texture("Miku_Clothes.png", TextureType.BASE_COLOR, tex_path)
    _01_mat.add_texture(white_tex, TextureType.TOON)

    outline_mat.add_texture(white_tex, TextureType.TOON)

    miku_material_map = {
        "Skin": skin_mat,
        "Clothes": clothes_mat,
        "Clothes2": clothes2_mat,
        "Glow": glow_mat,
        "Skirt": clothes2_mat,
        "Panel": panel_mat,
        "Tie": tie_mat,
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

    renderer.load_model('Miku/Genoge/MikuTest.obj', color=miku_color, transform=Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)), material=miku_material, material_map=miku_material_map)
    #renderer.load_model('Miku/Genoge/miku.obj', color = miku_color, transform = Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)), material=miku_material, material_map=miku_material_map)

def render_sour_miku():
    miku_color = [134, 206, 203, 255]
    face_mat = Material(kd=Vec3(0.95, 0.95, 0.95), ks=Vec3(0.03, 0.03, 0.03))
    body_mat = Material(kd=Vec3(0.95, 0.95, 0.95), ks=Vec3(0.03, 0.03, 0.03))
    口_mat = Material(ks=Vec3(0.25, 0.25, 0.25))
    目_mat = Material(kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.3, 0.3, 0.3), r=2.0)
    瞳_mat = Material(kd=Vec3(0.7, 0.7, 0.7), ks=Vec3(0.3, 0.3, 0.3), r=2.0)
    
    HL_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    髮_mat = Material(ks=Vec3(0.1, 0.1, 0.1))
    メガネ_mat = Material(ks=Vec3(0.2, 0.2, 0.2), r=6.0)
    白_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    黑裙里_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)

    绿裙_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    绿_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    绿光_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    红_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    pants_mat = Material(ks=Vec3(0.1, 0.1, 0.1))

    _01_mat = Material(ks=Vec3(0.3, 0.3, 0.3), r=6.0)
    髮影_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    照れ_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    涙_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)
    镜片_mat = Material(ks=Vec3(0.1, 0.1, 0.1), r=6.0)

    white_tex = "textures/white_tex.png"
    tex_path = "Miku/Sour/Tex"
    face_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    face_mat.add_texture(white_tex, TextureType.TOON)
    face_mat.enable_toon_edge(toon_edge_color=Vec4(0.576, 0.310, 0.553, 1.0), toon_edge_size=.0004)
    body_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    #body_mat.add_texture("toon_skin.png", TextureType.TOON, tex_path)
    body_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Skin.png", TextureType.TOON)
    body_mat.enable_toon_edge(toon_edge_color=Vec4(0.576, 0.310, 0.553, 1.0), toon_edge_size=.0004)
    口_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    口_mat.add_texture(white_tex, TextureType.TOON)
    口_mat.enable_toon_edge(toon_edge_color=Vec4(0.576, 0.310, 0.553, 1.0), toon_edge_size=.0003)
    目_mat.add_texture("eye3.png", TextureType.BASE_COLOR, tex_path)
    目_mat.add_texture(white_tex, TextureType.TOON)
    瞳_mat.add_texture("eye3.png", TextureType.BASE_COLOR, tex_path)
    瞳_mat.add_texture(white_tex, TextureType.TOON)
    
    HL_mat.add_texture("eye3.png", TextureType.BASE_COLOR, tex_path)
    HL_mat.add_texture(white_tex, TextureType.TOON)
    髮_mat.add_texture("hair.png", TextureType.BASE_COLOR, tex_path)
    #髮_mat.add_texture("toon_hair.png", TextureType.TOON, tex_path)
    髮_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Hair.png", TextureType.TOON)
    髮_mat.add_texture("sphere_hair.png", TextureType.SPHERE, tex_path)
    髮_mat.enable_toon_edge(toon_edge_color=Vec4(0.137, 0.345, 0.580, 1.0), toon_edge_size=.0004)
    メガネ_mat.add_texture("other.png", TextureType.BASE_COLOR, tex_path)
    メガネ_mat.add_texture(white_tex, TextureType.TOON)
    メガネ_mat.enable_toon_edge(toon_edge_color=Vec4(0.376, 0.204, 0.545, 1.0), toon_edge_size=.0004)
    白_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #白_mat.add_texture("toon_W.png", TextureType.TOON, tex_path)
    白_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Clothes.png", TextureType.TOON)
    白_mat.enable_toon_edge(toon_edge_color=Vec4(0.376, 0.204, 0.545, 1.0), toon_edge_size=.0004)
    黑裙里_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #黑裙里_mat.add_texture("toon_W.png", TextureType.TOON, tex_path)
    黑裙里_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Clothes.png", TextureType.TOON)

    绿裙_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #绿裙_mat.add_texture("toon_hair.png", TextureType.TOON, tex_path)
    绿裙_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Hair.png", TextureType.TOON)
    绿_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #绿_mat.add_texture("toon_hair.png", TextureType.TOON, tex_path)
    绿_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Hair.png", TextureType.TOON)
    绿_mat.enable_toon_edge(toon_edge_color=Vec4(0.137, 0.345, 0.580, 1.0), toon_edge_size=.0004)
    绿光_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #绿光_mat.add_texture("toon_hair.png", TextureType.TOON, tex_path)
    绿光_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Hair.png", TextureType.TOON)
    绿光_mat.enable_toon_edge(toon_edge_color=Vec4(0.137, 0.345, 0.580, 1.0), toon_edge_size=.0004)
    红_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    红_mat.add_texture(white_tex, TextureType.TOON)
    pants_mat.add_texture("W.png", TextureType.BASE_COLOR, tex_path)
    #pants_mat.add_texture("toon_W.png", TextureType.TOON, tex_path)
    pants_mat.add_texture("Miku/Genoge/Tex_Miku/Toon_Clothes.png", TextureType.TOON)
    pants_mat.enable_toon_edge(toon_edge_color=Vec4(0.549, 0.514, 0.722, 1.0), toon_edge_size=.0004)

    _01_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    _01_mat.add_texture(white_tex, TextureType.TOON)
    髮影_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    髮影_mat.add_texture(white_tex, TextureType.TOON)
    照れ_mat.add_texture("skin.png", TextureType.BASE_COLOR, tex_path)
    照れ_mat.add_texture(white_tex, TextureType.TOON)
    涙_mat.add_texture("eye3.png", TextureType.BASE_COLOR, tex_path)
    涙_mat.add_texture(white_tex, TextureType.TOON)
    镜片_mat.add_texture("other.png", TextureType.BASE_COLOR, tex_path)
    镜片_mat.add_texture(white_tex, TextureType.TOON)

    sour_miku_material_map = {
        "face" : face_mat,
        "body" : body_mat,
        "口" : 口_mat,
        "目" : 目_mat,
        "瞳" : 瞳_mat,
        
        "HL" : HL_mat,
        "髮" : 髮_mat,
        "メガネ" : メガネ_mat,
        "白" : 白_mat,
        "黑裙里" : 黑裙里_mat,

        "绿裙" : 绿裙_mat,
        "绿" : 绿_mat,
        "绿光" : 绿光_mat,
        "红" : 红_mat,
        "pants" : pants_mat,

        "01" : _01_mat,
        "髮影" : 髮影_mat,
        "照れ" : 照れ_mat,
        "涙" : 涙_mat,
        "镜片" : 镜片_mat
    }
    miku_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.6, 0.6, 0.6), ks=Vec3(0.25, 0.25, 0.25), r=10.0)
    renderer.load_model('Miku/Sour/Sour.obj', color=miku_color, transform=Mat4.from_translation(Vec3(0, -20, 0)) @ Mat4.from_scale(Vec3(20, 20, 20)), material=miku_material, material_map=sour_miku_material_map)

def render_rock():
    tex_path = 'Free_rock/Free_rock_tex'
    free_rock_material = Material(ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.5, 0.5, 0.5), ks=Vec3(0.8, 0.8, 0.8), r=6.0)
    free_rock_material.add_texture("Free_rock_Base_Color.jpg", TextureType.BASE_COLOR, tex_path)
    free_rock_material.add_texture("Free_rock_Mixed_AO.jpg", TextureType.AO, tex_path)
    free_rock_material.add_texture("Free_rock_Specular.jpg", TextureType.SPECULAR, tex_path)
    free_rock_material.add_texture("Free_rock_Roughness.jpg", TextureType.ROUGHNESS, tex_path)
    free_rock_material.add_texture("Free_rock_Normal_OpenGL.jpg", TextureType.NORMAL_MAP, tex_path)
    renderer.load_model('Free_rock/Free_rock.obj', color=[190, 190, 190, 255], material=free_rock_material)
    free_rock_material.use_gamma_correction = False


if __name__ == '__main__':
    width = 1280
    height = 720

    print("1 - Rock")
    print("2 - Genoge Miku")
    print("3 - Sour Miku")
    while True:
        n = int(input("Select a model # to render: "))

        if n not in [1, 2, 3]:
            print("Invalid input.")
        else:
            break

    # Render window.
    renderer = RenderWindow(width, height, "Custom Model Viewer", resizable = True)
    renderer.set_location(200, 200)
    controller = Control(renderer)

    match n:
        case 1:
            print("Rendering Rock...")
            render_rock()
        case 2:
            print("Rendering Genoge Miku...")
            render_genoge_miku()
        case 3:
            print("Rendering Sour Miku...")
            render_sour_miku()

    renderer.add_point_light(position=Vec3(100, 80, 100), intensity=1.0, has_attenuation=False)
    #renderer.add_point_light(position=Vec3(30, 30, 30), intensity=0.8)
    #renderer.add_point_light(position=Vec3(-10, 20, 20), intensity=0.2)
    #renderer.add_point_light(position=Vec3(-10, -20, 20), intensity=0.1)

    #renderer.add_area_light(width=40, depth=40, interval=5, transform=Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)
    #renderer.add_area_light(40, 40, 5, transform=Mat4.from_rotation(angle=0.785, vector=Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(0, 50, 0)), intensity=0.03)

    #draw shapes
    renderer.run()
