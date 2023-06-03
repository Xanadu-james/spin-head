import numpy as np
from matrix import *

class Camera(object):
    def __init__(self,eye,at,viewSize):
        self.eye = np.array(eye,'f')
        atArray = np.array(at,'f')
        self.resetMatProj(viewSize)
        self.matView = lookAt(self.eye,atArray, np.array([0.0,1.0,0.0],'f'))

    def resetMatProj(self,viewSize):
         self.matProj = perspective(np.pi/4.0, viewSize[0]/viewSize[1], 1, 500.0)
    
