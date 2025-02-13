#version 330 core

layout (location = 0) out vec4 fragColor;

// Structs needed for the shader
struct textArray {
    sampler2DArray array;
};

struct Material {
    vec3  color;
    float roughness;
    float subsurface;
    float sheen;
    float sheenTint;
    float anisotropic;
    float specular;
    float metallicness;
    float specularTint;
    float clearcoat;
    float clearcoatGloss;
    
    int   hasAlbedoMap;
    vec2  albedoMap;
    int   hasNormalMap;
    vec2  normalMap;
    int   hasRoughnessMap;
    vec2  roughnessMap;
    int   hasAoMap;
    vec2  aoMap;
};
in vec2 uv;
in mat3 TBN;

// Material attributes
flat in Material mtl;

// Uniforms
uniform textArray textureArrays[5];


vec3 getNormal(Material mtl, mat3 TBN){
    // Isolate the normal vector from the TBN basis
    vec3 normal = TBN[2];
    // Apply normal map if the material has one
    if (bool(mtl.hasNormalMap)) {
        normal = texture(textureArrays[int(round(mtl.normalMap.x))].array, vec3(uv, round(mtl.normalMap.y))).rgb * 2.0 - 1.0;
        normal = normalize(TBN * normal); 
    }
    // Return vector
    return normal;
}

uniform sampler2D depthMap;
uniform vec2 viewportDimensions;

void main() {


    vec2 uv = (gl_FragCoord.xy) / viewportDimensions;
    vec3 normal;

    float mappedDepth = texture(depthMap, uv).r;

    if (gl_FragCoord.z < mappedDepth){
        discard;
    }
    else{
        normal = getNormal(mtl, TBN);
        fragColor = vec4(normal/2 + 0.5, 1.0);
    }
}