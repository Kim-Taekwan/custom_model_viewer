from pyglet.graphics.shader import Shader, ShaderProgram
from enum import Enum

class ShaderMode(Enum):
    WIREFRAME = 1
    PHONG = 2
    GOURAUD = 3
    TEXTURED = 4
    NORMALMAP = 5

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
};

uniform int numLights;
uniform PointLight lights[10];
uniform vec3 viewPosition;

void main()
{
    vec4 worldPosition = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * worldPosition; // local->world->vp

    vec3 lightColor = vec3(0.0);
    vec3 N = normalize(mat3(model) * normals);
    vec3 V = normalize(viewPosition - worldPosition.xyz);
    vec3 k_a = vec3(0.1); // ambient coefficient
    vec3 k_d = vec3(0.5); // diffuse coefficient
    vec3 k_s = vec3(0.8); // specular coefficient
    float n = 8.0; // shininess parameter

    for (int i = 0; i < min(numLights, 10); i++) {
        vec3 lightVector = lights[i].position - worldPosition.xyz;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 R = reflect(-L, N);

        float attenuation = 1.0; // Suppose sunlight
        vec3 radiance = lights[i].color * lights[i].intensity;

        vec3 diffuse = attenuation * radiance * k_d * max(dot(N, L), 0.0);
        vec3 specular = attenuation * radiance * k_s * pow(max(dot(R, V), 0.0), n);
        vec3 ambient = k_a * radiance;

        lightColor += ambient + diffuse + specular;
    }

    vec3 color = colors.rgb * lightColor;
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
    newNormal = normalize(mat3(model) * normals);
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
};

uniform int numLights;
uniform PointLight lights[10];
uniform vec3 viewPosition;

void main()
{
    vec3 lightColor = vec3(0.0);
    vec3 N = normalize(newNormal);
    vec3 V = normalize(viewPosition - newPosition);
    vec3 k_a = vec3(0.1); // ambient coefficient
    vec3 k_d = vec3(0.5); // diffuse coefficient
    vec3 k_s = vec3(0.8); // specular coefficient
    float n = 8.0; // shininess parameter

    for (int i = 0; i < min(numLights, 10); i++) {
        vec3 lightVector = lights[i].position - newPosition;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 R = reflect(-L, N);

        float attenuation = 1.0; // Suppose sunlight
        vec3 radiance = lights[i].color * lights[i].intensity;

        vec3 diffuse = attenuation * radiance * k_d * max(dot(N, L), 0.0);
        vec3 specular = attenuation * radiance * k_s * pow(max(dot(R, V), 0.0), n);
        vec3 ambient = k_a * radiance;

        lightColor += ambient + diffuse + specular;
    }

    vec3 color = newColor.rgb * lightColor;
    outColor = vec4(color, newColor.a);
}
"""


# Textured Phong illumination shader sources
vertex_source_textured = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec3 normals;
layout(location =2) in vec2 tex_coords;
layout(location = 3) in vec3 tangents;

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

    vec3 N = newNormal;
    vec3 T = normalize(transpose(inverse(mat3(model))) * tangents);
    T = normalize(T - dot(T, N) * N);
    vec3 B = normalize(cross(N, T));

    TBN = mat3(T, B, N);
}
"""

fragment_source_textured = """
#version 330
in vec3 newNormal;
in vec3 newPosition;
in vec2 newTexCoords;
in mat3 TBN;

out vec4 outColor;

struct PointLight {
    vec3 position;
    vec3 color;
    float intensity;
};

uniform int numLights;
uniform PointLight lights[10];
uniform vec3 viewPosition;

uniform sampler2D baseColorTex;
uniform sampler2D mixedAoTex;
uniform sampler2D specularTex;
uniform sampler2D roughnessTex;
uniform sampler2D normalTex;
uniform bool useNormalMapping;

void main()
{
    vec3 baseColor = texture(baseColorTex, newTexCoords).rgb;
    vec3 mixedAo = texture(mixedAoTex, newTexCoords).rgb;
    vec3 specular = texture(specularTex, newTexCoords).rgb;
    float roughness = texture(roughnessTex, newTexCoords).x;

    vec3 N;
    if (useNormalMapping) {
        vec3 tangentNormal = texture(normalTex, newTexCoords).rgb;
        tangentNormal = 2.0 * tangentNormal - 1.0;
        N = normalize(TBN * tangentNormal);
    } else {
        N = normalize(newNormal);
    }
    vec3 V = normalize(viewPosition - newPosition);
    vec3 k_a = mixedAo * baseColor;
    vec3 k_d = baseColor;
    vec3 k_s = specular;
    float n = 1.0 / (0.02 * roughness + 0.001);

    vec3 color = vec3(0.0);
    for (int i = 0; i < min(numLights, 10); i++) {
        vec3 lightVector = lights[i].position - newPosition;
        float distance = length(lightVector);
        vec3 L = normalize(lightVector);
        vec3 R = reflect(-L, N);

        float attenuation = 1.0; // Suppose sunlight
        vec3 radiance = lights[i].color * lights[i].intensity;

        vec3 diffuse = attenuation * radiance * k_d * max(dot(N, L), 0.0);
        vec3 specular = attenuation * radiance * k_s * pow(max(dot(R, V), 0.0), n);
        vec3 ambient = k_a * radiance;

        color += ambient + diffuse + specular;
    }

    outColor = vec4(color, 1.0);
}
"""


def create_program(vs_source, fs_source):
    # compile the vertex and fragment sources to a shader program
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)