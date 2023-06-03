from OpenGL.GL import *

class Shader(object):
    def __init__(self,vsFile,fsFile):
        vs = self.createShader(vsFile, GL_VERTEX_SHADER)
        fs = self.createShader(fsFile, GL_FRAGMENT_SHADER)
        self.program = glCreateProgram()
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)
        glLinkProgram(self.program)

    def createShader(self,shaderFile, shaderType):
        with open(shaderFile, 'r') as file:
            source = file.read()
            shader = glCreateShader(shaderType)
            glShaderSource(shader, source)
            glCompileShader(shader)
            return shader

    