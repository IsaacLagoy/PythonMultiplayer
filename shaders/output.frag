#version 330 core

out vec4 fragColor;

in vec2 uv;

uniform sampler2D dimensionMap;
uniform sampler2D plainView;
uniform sampler2D sightView;

// uniform sampler2D dimDepthTex;
// uniform sampler2D plainDepthTex;

void main()
{ 


    float dim = texture(dimensionMap, uv).r;
    vec3 plain = texture(plainView, uv).rgb;
    vec3 sight = texture(sightView, uv).rgb;

    fragColor = vec4(mix(plain, sight, dim), 1.0);

    // float dimDepth = texture(dimDepthTex, uv).r;
    // float plainDepth = texture(plainDepthTex, uv).r;

    // if (plainDepth < dimDepth) {
    //     fragColor = vec4(plain, 1.0);
    // }
    // else {
    //     fragColor = vec4(mix(plain, sight, dim), 1.0);
    // }
}