
import math
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL import *
from objfile import *
from shader import *
from matrix import *
from camera import *

windowSize = [800,600]

shader = None
objFile = None
camera = None

lightDirection = np.array([0,1,1], 'f')
lightDirection /= np.linalg.norm(lightDirection)

ambientLight = np.array([0.1,0.1,0.1], 'f')
diffuseLight = np.array([0.8,0.8,0.8], 'f')
specularLight = np.array([1,1,1], 'f')


worldMatrix = np.identity(4,dtype='f')

def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
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

    glutSwapBuffers()

    
def reshape(w, h):
    windowSize = [w,h]
    glViewport(0,0,w, h);
    camera.resetMatProj(windowSize)

def rotate(x,y):
    global worldMatrix
    centerX = windowSize[0]/2
    centerY = windowSize[1]/2

    dx = x - centerX;
    dy = y - centerY;

    r = math.sqrt(dx * dx + dy * dy)
    alpha = math.acos(dy / r)
    if dx < 0: 
        alpha = -alpha
    worldMatrix = rotationYMatrix(alpha)


def mouse(button, state, x, y):
    rotate(x,y)

def mouseMotion(x, y):
    rotate(x,y)

if __name__ == "__main__":
    glutInit([])


    #glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)#|GLUT_3_2_CORE_PROFILE)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA|GLUT_3_2_CORE_PROFILE)
    glutInitWindowSize(windowSize[0], windowSize[1])
    glutCreateWindow(b"stage")

    #print(glGetString(GL_VENDOR).decode("utf-8"))
    #print(glGetString(GL_RENDERER).decode("utf-8"))
    print(glGetString(GL_VERSION).decode("utf-8"))
    print(glGetString(GL_SHADING_LANGUAGE_VERSION).decode("utf-8"))
    #print(glGetIntegerv(GL_NUM_EXTENSIONS))
    #print(glGetString(GL_EXTENSIONS))

    # glutInitContextVersion(4,3)
    # glutInitContextProfile(GLUT_CORE_PROFILE)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse);
    glutMotionFunc(mouseMotion);

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_CULL_FACE)
    #glDisable(GL_CULL_FACE)
    #glEnableClientState(GL_VERTEX_ARRAY)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    windowSize = [glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT)]

    camera = Camera([0.0,100.0,500.0],[0.0,100.0,0.0],windowSize)

    shader = Shader("./shader/vs.glsl","./shader/fs.glsl")
    objFile = ObjFile()
    objFile.load("./res/head.obj")

    glutMainLoop()


