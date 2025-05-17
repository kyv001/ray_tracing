from pygame.math import *
from others import *
from tqdm import tqdm
import multiprocessing

class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def render(self, screen, things):
        color = screen.pos * 1
        q = multiprocessing.Queue(maxsize=1024)
        def _render(offset, size, screen, things, q):
            for x in tqdm(range(offset[0], offset[0] + size[0])):
                for y in range(offset[1], offset[1] + size[1]):
                    d = (screen.pos[y][x] - Vector3(self.x, self.y, self.z)).normalize()
                    d_last = inf
                    for thing in things:
                        c, distance = thing.get_color(Vector3(self.x, self.y, self.z), d, things, 0)
                        if distance < d_last:
                            q.put((x, y, list(c)))
                            d_last = distance
            q.put(None)
        
        processes = []
        n_groups = 64
        assert (n_groups ** 0.5).is_integer()
        n_xgoups = n_ygoups = int(n_groups ** 0.5)
        for ia in range(n_xgoups):
            for ib in range(n_ygoups):
                offset = [ia * screen.length // n_xgoups, ib * screen.height // n_xgoups]
                size = [screen.length // n_xgoups, screen.height // n_xgoups]
                process = multiprocessing.Process(target=_render, args=(offset, size, screen, things, q))
                process.start()
                processes.append(process)
        
        finish_count = 0
        while finish_count < n_groups:
            d = q.get()
            if d is None:
                finish_count += 1
            else:
                (x, y, c) = d
                for i in range(3):
                    c[i] = max(0, c[i])
                color[y][x] = c

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




