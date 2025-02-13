#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D plainDepthTex;
uniform vec2 viewportDimensions;


void main() {
    vec2 uv = (gl_FragCoord.xy) / viewportDimensions;
    float plainDepth = texture(plainDepthTex, uv).r;

    if (gl_FragCoord.z > plainDepth) { discard; }
    
    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
}