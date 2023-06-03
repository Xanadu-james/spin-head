import numpy as np

def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan( fov / 2 )
    d = far - near
    return np.array([
		    [f / aspect, 0.0, 0.0, 0.0],
		    [0.0, f, 0.0, 0.0],
		    [0.0, 0.0, -(near + far) / d, -2 * near * far / d],
		    [0.0, 0.0, -1, 0.0]],'f')

def lookAt(eye, at, up):
    v = at - eye
    v = v / np.linalg.norm(v)

    n = np.cross(v, up)
    n = n / np.linalg.norm(n)

    u = np.cross(n, v)
    u = u / np.linalg.norm(u)

    v = -v
    return np.array([
		[n[0], n[1], n[2], -np.dot(n, eye)],
		[u[0], u[1], u[2], -np.dot(u, eye)],
		[v[0], v[1], v[2], -np.dot(v, eye)],
		[0.0, 0.0, 0.0, 1.0]],'f')


def scaleMatrix(s):
    S = np.identity(4,dtype='f')
    S[0,0] = s[0];
    S[1,1] = s[1];
    S[2,2] = s[2];
    return S

def rotationYMatrix(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    R = np.identity(4,dtype='f')
    R[0,0] = c
    R[0,2] = s
    R[2,0] = -s
    R[2,2] = c
    return R
