#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;

out vec3 fPosition;
out vec3 fNormal;

uniform mat4 projMatrix;
uniform mat4 viewMatrix;
uniform mat4 worldMatrix;

void main(){
    vec4 pos = worldMatrix * vec4(aPosition, 1.0f);
    gl_Position = projMatrix * viewMatrix * pos;
    fPosition = pos.xyz;
    vec4 n = worldMatrix * vec4(aNormal,0.0f);
    fNormal = n.xyz;
}
