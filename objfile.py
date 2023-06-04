import os
import numpy as np
from OpenGL.GL import *

class ObjMaterial(object):
    def __init__(self):
        self.Kd = np.array([1,1,1], 'f')
        self.Ks = np.array([1,1,1], 'f')
        self.Ka = np.array([1,1,1], 'f')
        self.Ns = 32.0
        self.d = 1.0

class ObjMesh(object):
    def __init__(self,mtlName,positions,normals):
        self.material = ObjMaterial()
        self.materialName = mtlName
        self.verticesCount = len(positions)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER , vbo[0])
        glBufferData(GL_ARRAY_BUFFER , np.array(positions,dtype="float32") , GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER , vbo[1])
        glBufferData(GL_ARRAY_BUFFER , np.array(normals,dtype="float32") , GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER,0)

    def render(self,program):
        glUniform3fv(glGetUniformLocation(program, "Ka"), 1, self.material.Ka)
        glUniform3fv(glGetUniformLocation(program, "Kd"), 1, self.material.Kd)
        glUniform3fv(glGetUniformLocation(program, "Ks"), 1, self.material.Ks)
        glUniform1f(glGetUniformLocation(program, "Ns"), self.material.Ns)
        glUniform1f(glGetUniformLocation(program, "d"), self.material.d)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.verticesCount)



class ObjFile(object):
    def __init__(self):
        self.materials = {}
        self.meshs = []

    def loadMaterial(self,fileName):
        mtl = None
        with open(fileName, 'r') as file:
            for line in file:
                if line.startswith('#'): 
                    continue
                values = line.split()
                if not values: 
                    continue
                if values[0] == 'newmtl':
                    mtl = ObjMaterial()
                    self.materials[values[1]] = mtl
                elif mtl:
                     if values[0] == 'Kd':
                         mtl.Kd = np.array([ float(x) for x in values[1:4] ], 'f') 
                     elif values[0] == 'Ks':
                         mtl.Ks = np.array([ float(x) for x in values[1:4] ], 'f') 
                     elif values[0] == 'Ka':
                         mtl.Ka = np.array([ float(x) for x in values[1:4] ], 'f') 
                     elif values[0] == 'Ns':
                         mtl.Ns = float(values[1])
                     elif values[0] == 'd':
                         mtl.d = float(values[1])
                    
    def createMesh(self,mtlName, positions,normals):
        if len(positions) < 3: 
            return
        self.meshs.append(ObjMesh(mtlName,positions,normals))


    def load(self,fileName):
        with open(fileName, 'r') as file:
            vs = []
            vns = []
            mtlName = ""
            positions = []
            normals = []
            for line in file:
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                if values[0] == 'v':
                    vs.append([ float(x) for x in values[1:4]])
                elif values[0] == 'vn':
                    vns.append([ float(x) for x in values[1:4]])
                elif values[0] == 'usemtl':
                    self.createMesh(mtlName, positions,normals)
                    positions = []
                    normals = []
                    mtlName = values[1]
                elif values[0] == 'mtllib':
                    mtlPath = os.path.split(fileName)[0] + "/" + values[1];
                    self.loadMaterial(mtlPath)
                elif values[0] == 'f':
                    face = []
                    for v in values[1:]:
                        f = v.split('/')
                        face.append([int(f[0]),int(f[2])])

                    for i in range(1,len(face)-1):
                        positions.append(vs[face[0][0]-1])
                        positions.append(vs[face[i][0]-1])
                        positions.append(vs[face[i+1][0]-1])

                        normals.append(vns[face[0][1]-1])
                        normals.append(vns[face[i][1]-1])
                        normals.append(vns[face[i+1][1]-1])
            self.createMesh(mtlName, positions,normals)

            for mesh in self.meshs:
                if self.materials.__contains__(mesh.materialName) == True:
                    mesh.material = self.materials[mesh.materialName]
            self.meshs = sorted(self.meshs, key = lambda x : x.material.d,reverse=True)
                
    def render(self,program):
        for mesh in self.meshs:
            mesh.render(program)
