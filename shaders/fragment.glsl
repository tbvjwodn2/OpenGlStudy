#version 330 core

// in vec3 fragColor;
in vec2 fragTexCoord;

out vec4 color;

uniform sampler2D imageTexture;

void main()
{
    color = texture(imageTexture, fragTexCoord);
    // color = vec4(fragColor,1.0) * texture(imageTexture, fragTexCoord);
}