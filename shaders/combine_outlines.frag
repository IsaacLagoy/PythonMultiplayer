#version 330 core

out vec4 fragColor;

in vec2 uv;

uniform sampler2D baseOutline;
uniform sampler2D otherOutline;

// uniform sampler2D dimDepthTex;
// uniform sampler2D plainDepthTex;


void main()
{ 
    fragColor = texture(baseOutline, uv) - (1 - texture(otherOutline, uv));;

    // float dimDepth = texture(dimDepthTex, uv).r;
    // float plainDepth = texture(plainDepthTex, uv).r;

    // if (plainDepth < dimDepth) {
    //     fragColor -= (1 - texture(otherOutline, uv));
    // }
}