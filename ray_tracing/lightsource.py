from pygame.math import *
from others import *

class LightSource:
    def __init__(self, x, y, z, r, c):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.c = c

    def get_color(self, p_r, d_r, things, t):
        a = Vector3(self.x, self.y, self.z) - p_r
        
        l = d_r.dot(a)
        aa = a.dot(a)
        rr = self.r ** 2

        if aa > rr and l < 0:
            return [0, 0, 0], inf

        mm = aa - l ** 2
        if mm >= rr:
            return [0, 0, 0], inf
        q = (rr - mm) ** 0.5
        if aa > rr:
            t_ = l - q
        else:
            t_ = l + q

        return self.c, t_

