import pygame
import random
import time
from pygame.math import *
from others import *
import multiprocessing

class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def render(self, screen, things, window):
        color = screen.pos * 1
        q = multiprocessing.Queue(maxsize=1024)
        def _render(offset, size, screen, things, q):
            dots = [
                (x, y)
                for x in range(offset[0], min(offset[0] + size[0], screen.length))
                for y in range(offset[1], min(offset[1] + size[1], screen.height))
            ]
            random.shuffle(dots)
            for x, y in dots:
                d = (screen.pos[y][x] - Vector3(self.x, self.y, self.z)).normalize()
                d_last = inf
                for thing in things:
                    c, distance = thing.get_color(Vector3(self.x, self.y, self.z), d, things, 0)
                    if distance < d_last:
                        q.put((x, y, list(c)))
                        d_last = distance
            q.put(None)
        
        processes = []
        n_xgoups = 30
        n_ygoups = 30
        n_groups = n_xgoups * n_ygoups
        for ia in range(n_xgoups):
            for ib in range(n_ygoups):
                offset = [ia * screen.length // n_xgoups, ib * screen.height // n_ygoups]
                size = [screen.length // n_xgoups + 1, screen.height // n_ygoups + 1]
                process = multiprocessing.Process(target=_render, args=(offset, size, screen, things, q))
                process.start()
                processes.append(process)
        
        finish_count = 0
        t0 = time.perf_counter()
        while finish_count < n_groups:
            d = q.get()
            if d is None:
                finish_count += 1
                print(f"{finish_count/n_groups*100:.2f}% finished\r", end="")
            else:
                (x, y, c) = d
                for i in range(3):
                    c[i] = round(max(0, min(255, c[i])))
                window.set_at((x, y), c)
                if time.perf_counter() - t0 > 0.1:
                    pygame.display.update()
                    t0 = time.perf_counter()
        
        return color




