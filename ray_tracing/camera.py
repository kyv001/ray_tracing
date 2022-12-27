from pygame.math import *
from others import *
from tqdm import tqdm

class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def render(self, screen, things):
        color = screen.pos * 1
        for x in tqdm(range(screen.length)):
            for y in range(screen.height):
                d = (screen.pos[y][x] - Vector3(self.x, self.y, self.z)).normalize()
                d_last = inf
                for thing in things:
                    c, distance = thing.get_color(Vector3(self.x, self.y, self.z), d, things, 0)
                    if distance < d_last:
                        color[y][x] = list(c)
                        d_last = distance
                
                for i in range(3):
                    color[y][x][i] = max(color[y][x][i], 0)

        m = 0
        for x in range(screen.length):
            for y in range(screen.height):
                for i in range(3):
                    if color[y][x][i] > m:
                        m = color[y][x][i]
                        
        for x in range(screen.length):
            for y in range(screen.height):
                for i in range(3):
                    color[y][x][i] /= m / 255
                    color[y][x][i] = round(color[y][x][i])
                        
        return color




