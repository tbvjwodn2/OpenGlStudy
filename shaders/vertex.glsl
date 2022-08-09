#version 330 core

layout (location=0) in vec3 vertexPos;
// layout (location=1) in vec3 vertexColor;
layout (location=1) in vec2 vertexTexCoord;
// layout (location=3) in vec3 vertexNormal;

// out vec3 fragColor;
// out vec3 fragVertNormal;

uniform mat4 model;
uniform mat4 projection;

out vec2 fragTexCoord;

void main()
{
    gl_Position = projection * model * vec4(vertexPos, 1.0);
    // fragColor = vertexColor;
    fragTexCoord = vertexTexCoord;
    // fragVertNormal = vertexNormal;
}
