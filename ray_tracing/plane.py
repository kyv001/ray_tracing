from random import gauss, randint
from pygame.math import *
from others import *

class Plane:
    def __init__(self, x, y, z, n, c, roughness, reflectivity, transparency):
        self.x = x
        self.y = y
        self.z = z
        self.n = n
        self.c = c
        self.roughness = roughness
        self.reflectivity = reflectivity
        self.transparency = transparency

    def get_color(self, p_r, d_r, things, t):
        if t > 10:
            return [0, 0, 0], inf
        dn = d_r.dot(self.n)
        if dn != 0:
            t_ = (Vector3(self.x, self.y, self.z) - p_r).dot(self.n) / dn
            if t_ > 0:
                p_next = p_r + d_r * t_
                reflected_n = Vector3(self.n[0] + gauss(0, 50) / 10000 * self.roughness, self.n[1] + gauss(0, 50) / 10000 * self.roughness, self.n[2] + gauss(0, 50) / 10000 * self.roughness)
                reflected_n = reflected_n.normalize()
                reflected_d = d_r - 2 * (d_r.dot(reflected_n)) * reflected_n
                color_reflected = self.c * 0
                d_last = inf
                for thing in things:
                    if thing != self:
                        c, distance = thing.get_color(p_next, reflected_d.normalize(), things, t + 1)
                        if distance < d_last:
                            color_reflected = c
                            d_last = distance
                            color_reflected = list(color_reflected)
                            
                p_next = p_r + d_r * t_
                through_n = self.n
                through_n = through_n.normalize()
                through_d = d_r
                color_through = self.c * 0
                d_last = inf
                for thing in things:
                    if thing != self:
                        c, distance = thing.get_color(p_next, through_d.normalize(), things, t + 1)
                        if distance < d_last:
                            color_through = c
                            d_last = distance
                            color_through = list(color_through)
                    
                color = [0, 0, 0]
                for i in range(3):
                    color[i] = \
                        color_through[i] / 255 * self.c[i] * self.transparency + \
                        (
                            color_reflected[i] / 255 * self.c[i] * self.reflectivity + \
                            self.c[i] * (1 - self.reflectivity) * ENV
                        ) * (1 - self.transparency)
                    
                return color, t_
        return [0, 0, 0], inf




