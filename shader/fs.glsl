#version 330 core

in vec3 fPosition;
in vec3 fNormal;

out vec4 fragColor;

uniform vec3 eye;

uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform float Ns;
uniform float d;

uniform vec3 lightDir;
uniform vec3 Ia;
uniform vec3 Id;
uniform vec3 Is;

void main() {
    vec3 l = lightDir;
    vec3 n = normalize(fNormal);

    vec3 ambient = Ia * Ka;
    vec3 diffuse = vec3(0.0f,0.0f,0.0f);
    vec3 specular = vec3(0.0f,0.0f,0.0f);

    float nl = dot(l, n);
    if(nl > 0.0f) {
        diffuse = Id * Kd * nl;
        vec3 r = reflect(-l, n);
        vec3 v = normalize(eye-fPosition);
        float rv = dot(r,v);
        if(rv > 0.0f) {
            specular = Is * Ks * pow(rv, Ns);
        }
    }

    fragColor = vec4(ambient + diffuse + specular,d);
}


