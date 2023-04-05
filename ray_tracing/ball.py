from random import gauss
from pygame.math import *
from others import *

class Ball:
    def __init__(self, x, y, z, r, c, roughness, reflectivity):
        self.x = x
        self.y = y
        self.z = z
        self.c = c
        self.r = r
        self.roughness = roughness
        self.reflectivity = reflectivity

    def get_color(self, p_r, d_r, things, t):
        if t > iterN:
            return [0, 0, 0], inf
        
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
            
        reflected_p = p_r + t_ * d_r
        
        color = [0, 0, 0]
        for _ in range(mcN):
            n = Vector3(reflected_p - Vector3(self.x, self.y, self.z))
            n = Vector3(n[0] + gauss(0, 50) / 10000 * self.roughness, n[1] + gauss(0, 50) / 10000 * self.roughness, n[2] + gauss(0, 50) / 10000 * self.roughness)
            n = n.normalize()
            reflected_d = d_r - 2 * (d_r.dot(n)) * n
            d_last = inf
            for thing in things:
                if thing != self:
                    c, distance = thing.get_color(reflected_p, reflected_d.normalize(), things, t + 1)
                    if distance < d_last:
                        d_last = distance
                        lc = list(c)
                        for i in range(3):
                            color[i] += lc[i] / mcN
                
        for i in range(3):
            color[i] = color[i] / 255 * self.c[i] * self.reflectivity + self.c[i] * (1 - self.reflectivity) * ENV
                
        return color, t_




