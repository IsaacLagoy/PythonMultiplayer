
#version 330 core
out vec4 fragColor;
  

in vec2 uv;
uniform sampler2D screenTexture;

uniform vec2 viewportDimensions;


void main()
{ 
    float offset = 1.0 / viewportDimensions.x;  

    vec2 offsets[9] = vec2[](
        vec2(-offset,  offset), // top-left
        vec2( 0.0f,    offset), // top-center
        vec2( offset,  offset), // top-right
        vec2(-offset,  0.0f),   // center-left
        vec2( 0.0f,    0.0f),   // center-center
        vec2( offset,  0.0f),   // center-right
        vec2(-offset, -offset), // bottom-left
        vec2( 0.0f,   -offset), // bottom-center
        vec2( offset, -offset)  // bottom-right    
    );

    float kernel[9] = float[](
        1, 1, 1,
        1,-8, 1,
        1, 1, 1
    );
    

    vec3 sampleTex[9];
    for(int i = 0; i < 9; i++)
    {
        sampleTex[i] = texture(screenTexture, uv.xy + offsets[i]).rgb;
    }
    vec3 col = vec3(0.0);
    for(int i = 0; i < 9; i++)
        col += sampleTex[i] * kernel[i];

    // float line = dot(col, vec3(1.0, 1.0, 1.0));

    vec4 outline = vec4(0.0, 0.0, 0.0, 1.0);

    float t = .05;
    if (col.r > t || col.g > t || col.b > t){
        outline.rgb = vec3(1.0);
    }

    fragColor = vec4(vec3(1.0) - outline.rgb, 1.0);

    // fragColor = outline;
}
