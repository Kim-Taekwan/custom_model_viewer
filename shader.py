from pyglet.graphics.shader import Shader, ShaderProgram
from enum import Enum

class ShaderMode(Enum):
    DEFAULT = 0
    WIREFRAME = 1
    GOURAUD = 2
    PHONG = 3
    BLINN_PHONG = 4
    TEXTURED = 5
    TOON_EDGE = 6

# create vertex and fragment shader sources
vertex_source_default = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;

out vec4 newColor;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    newColor = colors;
}
"""

fragment_source_default = """
#version 330
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""


# Gouraud illumination shader sources
vertex_source_gouraud = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 normals;

out vec4 newColor;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

struct PointLight {
    vec3 position;
    vec3 color;
    float intensity;
    bool hasAttenuation;
};

uniform int numLights;
uniform PointLight lights[1000];
uniform vec3 viewPosition;

void main()
{
    vec4 worldPosition = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * worldPosition; // local->world->vp

    vec3 N = normalize(transpose(inverse(mat3(model))) * normals);
    vec3 V = normalize(viewPosition - worldPosition.xyz);
    vec3 k_a = vec3(0.1); // ambient coefficient
    vec3 k_d = vec3(0.5); // diffuse coefficient
    vec3 k_s = vec3(0.8); // specular coefficient
    float n = 8.0; // shininess parameter

    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < min(numLights, 1000); i++) {
        vec3 lightVector = lights[i].position - worldPosition.xyz;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 R = reflect(-L, N);

        float attenuation = lights[i].hasAttenuation ? 1 / (1 + 0.001 * distance + 0.00005 * distance * distance) : 1;
        vec3 radiance = lights[i].color * lights[i].intensity;

        diffuse += attenuation * radiance * k_d * max(dot(N, L), 0.0);
        specular += attenuation * radiance * k_s * pow(max(dot(R, V), 0.0), n);
        ambient += k_a * radiance;
    }

    vec3 color = colors.rgb * (ambient + diffuse) + specular;
    newColor = vec4(color, colors.a);
}
"""

fragment_source_gouraud = """
#version 330
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""


# Phong illumination shader sources
vertex_source_phong = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 normals;

out vec4 newColor;
out vec3 newNormal;
out vec3 newPosition;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    vec4 worldPosition = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * worldPosition; // local->world->vp
    newColor = colors;
    newNormal = normalize(transpose(inverse(mat3(model))) * normals);
    newPosition = worldPosition.xyz;
}
"""

fragment_source_phong = """
#version 330
in vec4 newColor;
in vec3 newNormal;
in vec3 newPosition;

out vec4 outColor;

struct PointLight {
    vec3 position;
    vec3 color;
    float intensity;
    bool hasAttenuation;
};

uniform int numLights;
uniform PointLight lights[1000];
uniform vec3 viewPosition;

void main()
{
    vec3 N = normalize(newNormal);
    vec3 V = normalize(viewPosition - newPosition);
    vec3 k_a = vec3(0.1); // ambient coefficient
    vec3 k_d = vec3(0.5); // diffuse coefficient
    vec3 k_s = vec3(0.8); // specular coefficient
    float n = 8.0; // shininess parameter

    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < min(numLights, 1000); i++) {
        vec3 lightVector = lights[i].position - newPosition;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 R = reflect(-L, N);

        float attenuation = lights[i].hasAttenuation ? 1 / (1 + 0.001 * distance + 0.00005 * distance * distance) : 1;
        vec3 radiance = lights[i].color * lights[i].intensity;

        diffuse += attenuation * radiance * k_d * max(dot(N, L), 0.0);
        specular += attenuation * radiance * k_s * pow(max(dot(R, V), 0.0), n);
        ambient += k_a * radiance;
    }

    vec3 color = newColor.rgb * (ambient + diffuse) + specular;
    outColor = vec4(color, newColor.a);
}
"""


# Blinn-Phong illumination shader sources
vertex_source_blinn_phong = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 normals;

out vec4 newColor;
out vec3 newNormal;
out vec3 newPosition;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    vec4 worldPosition = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * worldPosition; // local->world->vp
    newColor = colors;
    newNormal = normalize(transpose(inverse(mat3(model))) * normals);
    newPosition = worldPosition.xyz;
}
"""

fragment_source_blinn_phong = """
#version 330
in vec4 newColor;
in vec3 newNormal;
in vec3 newPosition;

out vec4 outColor;

struct PointLight {
    vec3 position;
    vec3 color;
    float intensity;
    bool hasAttenuation;
};

uniform int numLights;
uniform PointLight lights[1000];
uniform vec3 viewPosition;

void main()
{
    vec3 N = normalize(newNormal);
    vec3 V = normalize(viewPosition - newPosition);
    vec3 k_a = vec3(0.1); // ambient coefficient
    vec3 k_d = vec3(0.5); // diffuse coefficient
    vec3 k_s = vec3(0.8); // specular coefficient
    float n = 24.0; // shininess parameter
    
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < min(numLights, 1000); i++) {
        vec3 lightVector = lights[i].position - newPosition;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 H = normalize(L + V);

        float attenuation = lights[i].hasAttenuation ? 1 / (1 + 0.001 * distance + 0.00005 * distance * distance) : 1;
        vec3 radiance = lights[i].color * lights[i].intensity;

        diffuse += attenuation * radiance * k_d * max(dot(N, L), 0.0);
        specular += attenuation * radiance * k_s * pow(max(dot(N, H), 0.0), n);
        ambient += k_a * radiance;
    }

    vec3 color = newColor.rgb * (ambient + diffuse) + specular;
    outColor = vec4(color, newColor.a);
}
"""


# Textured Phong illumination shader sources
vertex_source_material = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 normals;
layout(location =3) in vec2 tex_coords;
layout(location =4) in vec3 tangents;

out vec4 newColor;
out vec3 newNormal;
out vec3 newPosition;
out vec2 newTexCoords;
out mat3 TBN;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    vec4 worldPosition = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * worldPosition; // local->world->vp
    newNormal = normalize(transpose(inverse(mat3(model))) * normals);
    newPosition = worldPosition.xyz;
    newTexCoords = tex_coords;
    newColor = colors;

    vec3 N = newNormal;
    vec3 T = normalize(transpose(inverse(mat3(model))) * tangents);
    T = normalize(T - dot(T, N) * N);
    vec3 B = normalize(cross(N, T));

    TBN = mat3(T, B, N);
}
"""

fragment_source_material = """
#version 330
in vec4 newColor;
in vec3 newNormal;
in vec3 newPosition;
in vec2 newTexCoords;
in mat3 TBN;

out vec4 outColor;

struct PointLight {
    vec3 position;
    vec3 color;
    float intensity;
    bool hasAttenuation;
};

uniform int numLights;
uniform PointLight lights[1000];
uniform vec3 viewPosition;

uniform vec3 ka;
uniform vec3 kd;
uniform vec3 ks;
uniform float r;

uniform sampler2D baseColorTex;
uniform sampler2D mixedAoTex;
uniform sampler2D specularTex;
uniform sampler2D roughnessTex;
uniform sampler2D normalTex;
uniform sampler2D toonTex;
uniform sampler2D sphereTex;

uniform bool useBaseColor;
uniform bool useAO;
uniform bool useSpecular;
uniform bool useRoughness;
uniform bool useNormalMapping;
uniform bool useToon;
uniform bool useSphere;
uniform bool useGamma;

void main()
{
    vec4 texColor = texture(baseColorTex, newTexCoords);
    if (useBaseColor && texColor.a < 0.6)
        discard;

    float gamma = 1.0;
    if (useGamma) gamma = 2.2;
    vec3 baseColor = (useBaseColor ? pow(texColor.rgb, vec3(gamma)) : newColor.rgb);
    vec3 k_a = (useAO ? texture(mixedAoTex, newTexCoords).rgb * baseColor : ka);
    vec3 k_s = (useSpecular ? texture(specularTex, newTexCoords).rgb : ks);
    vec3 k_d = (useBaseColor ? baseColor : kd);
    float roughness = (useRoughness ? texture(roughnessTex, newTexCoords).x : r);
    float n = 1.0 / (0.003 * roughness + 0.001); // shininess parameter
    float alpha = useBaseColor ? texColor.a : newColor.a;

    vec3 N;
    if (useNormalMapping) {
        vec3 tangentNormal = texture(normalTex, newTexCoords).rgb;
        tangentNormal = 2.0 * tangentNormal - 1.0;
        N = normalize(TBN * tangentNormal);
    } else {
        N = normalize(newNormal);
    }
    vec3 V = normalize(viewPosition - newPosition);

    vec3 color = vec3(0.0);
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < min(numLights, 1000); i++) {
        vec3 lightVector = lights[i].position - newPosition;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        //vec3 R = reflect(-L, N);
        vec3 H = normalize(L + V);

        float attenuation = lights[i].hasAttenuation ? 1 / (1 + 0.001 * distance + 0.00005 * distance * distance) : 1;
        vec3 radiance = lights[i].color * lights[i].intensity;

        float ndotl = max(dot(N, L), 0.0);
        if (useToon) {
            //float stepped = ndotl > 0.55 ? 0.8 : (ndotl > 0.05 ? 0.6 : 0.3);
            //vec3 toonColor = texture(toonTex, vec2(0.5, stepped)).rgb;
            //diffuse += attenuation * radiance * k_d * stepped * toonColor;

            vec3 toonColor = texture(toonTex, vec2(0.5, ndotl)).rgb * 0.9;
            diffuse += attenuation * radiance * k_d * toonColor;
        }
        else {
            diffuse += attenuation * radiance * k_d * ndotl;
        }

        specular += attenuation * radiance * k_s * pow(max(dot(N, H), 0.0), n);
        ambient += k_a * radiance;
    }

    if (!useBaseColor) {
        color = newColor.rgb * (diffuse + ambient) + specular;
        color = pow(color, vec3(1/gamma));
    }
    else
        color = diffuse + specular + ambient;

    vec3 sphereColor = vec3(0.0);
    if (useSphere) {
        vec3 R = reflect(-V, N);
        vec2 sphereUV = R.xy * 0.5 + 0.5;
        sphereColor = texture(sphereTex, sphereUV).rgb;
        color += sphereColor * 0.2;
    }
    
    outColor = vec4(color, alpha);
}
"""


vertex_source_edge = """
#version 330
layout(location = 0) in vec3 vertices;
layout(location = 2) in vec3 normals;

uniform mat4 view_proj;
uniform mat4 model;
uniform float edgeWidth;

void main()
{
    vec3 expanded = vertices + normals * edgeWidth;
    gl_Position = view_proj * model * vec4(expanded, 1.0);
}
"""

fragment_source_edge = """
#version 330
out vec4 outColor;
uniform vec4 edgeColor;

void main()
{
    outColor = edgeColor;
}
"""


def create_program(vs_source, fs_source):
    # compile the vertex and fragment sources to a shader program
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)