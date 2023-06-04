import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from objfile import *
from shader import *
from matrix import *
from camera import *

windowSize = [800, 600]
window = None

shader = None
objFile = None
camera = None

lightDirection = np.array([0, 1, 1], 'f')
lightDirection /= np.linalg.norm(lightDirection)

ambientLight = np.array([0.1, 0.1, 0.1], 'f')
diffuseLight = np.array([0.8, 0.8, 0.8], 'f')
specularLight = np.array([1, 1, 1], 'f')

scaling = 50
worldMatrix = scaleMatrix([scaling,scaling,scaling])

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader.program)
    glUniformMatrix4fv(glGetUniformLocation(shader.program, "worldMatrix"), 1, True, worldMatrix)
    glUniformMatrix4fv(glGetUniformLocation(shader.program, "projMatrix"), 1, True, camera.matProj)
    glUniformMatrix4fv(glGetUniformLocation(shader.program, "viewMatrix"), 1, True, camera.matView)
    glUniform3fv(glGetUniformLocation(shader.program, "eye"), 1, camera.eye)
    glUniform3fv(glGetUniformLocation(shader.program, "lightDir"), 1, lightDirection)
    glUniform3fv(glGetUniformLocation(shader.program, "Ia"), 1, ambientLight)
    glUniform3fv(glGetUniformLocation(shader.program, "Id"), 1, diffuseLight)
    glUniform3fv(glGetUniformLocation(shader.program, "Is"), 1, specularLight)

    objFile.render(shader.program)

    pygame.display.flip()


def reshape(w, h):
    global windowSize
    windowSize = [w, h]
    glViewport(0, 0, w, h)
    camera.resetMatProj(windowSize)


def rotate(x, y):
    global worldMatrix
    centerX = windowSize[0] / 2
    centerY = windowSize[1] / 2

    dx = x - centerX
    dy = y - centerY

    r = math.sqrt(dx * dx + dy * dy)
    alpha = math.acos(dy / r)
    if dx < 0:
        alpha = -alpha
    worldMatrix = np.matmul(scaleMatrix([scaling,scaling,scaling]), rotationYMatrix(alpha))


def main():
    global window, shader, objFile, camera

    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                    pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode((640,480), pygame.OPENGL|pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_CULL_FACE)

    windowWidth, windowHeight = windowSize
    camera = Camera([0.0, 100.0, 500.0], [0.0, 100.0, 0.0], windowSize)

    shader = Shader("./shader/vs.glsl", "./shader/fs.glsl")
    objFile = ObjFile()
    objFile.load("./res/head.obj")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == VIDEORESIZE:
                reshape(event.w, event.h)
            elif event.type == MOUSEMOTION:
                rotate(event.pos[0], event.pos[1])

        draw()

        pygame.display.set_caption("Memoji! - FPS: %.2f" % clock.get_fps())
        clock.tick(60)

if __name__ == "__main__":
    main()
