from pygame.math import *
import numpy as np

class Screen:
    def __init__(self, center, length, height, size):
        length //= 2
        height //= 2
        self.pos = [
            [Vector3(x, y, center[2]) for x in np.arange(center[0] - length * size, center[0] + length * size, size)]
            for y in np.arange(center[1] - height * size, center[1] + height * size, size)]
        self.length = length * 2
        self.height = height * 2
        # print(self.pos)




