import pygame
from pygame.locals import *
from pygame.math import *

from camera import Camera
from plane import Plane
from screen import Screen
from lightsource import LightSource
from ball import Ball

pygame.init()
length = 1280
height = 720
camera = Camera(0, 0, 0)
plane = Plane(0, 3, 0, Vector3(0, 1, 0), Vector3(255, 255, 200), 3, 0.7, 0.3)
lightsource1 = LightSource(6, -3, 6, 0.1, (255, 255, 0))
lightsource2 = LightSource(-2, -4, 5, 0.1, (255, 255, 255))
lightsource3 = LightSource(-4, -1, 4, 0.1, (0, 255, 255))
ball1 = Ball(-3, -1, 8, 1, (0, 255, 255), 5, 0.8)
ball2 = Ball(-8, -2, 6, 1.5, (255, 0, 255), 0, 0.6)
ball3 = Ball(3, -12, 30, 12, (255, 255, 255), 5, 0.9)
ball4 = Ball(8, -1, 6, 1, (255, 255, 0), 0, 0.5)
ball5 = Ball(6, 12, 20, 5, (255, 125, 0), 0, 0.8)
screen = Screen((0, 0, 2), length, height, 0.012)
things = [lightsource1, lightsource2, lightsource3, plane, ball1, ball2, ball3, ball4, ball5]
#things = [lightsource1, plane]
rendered_screen = camera.render(screen, things)
window = pygame.display.set_mode((length, height))

for y in range(height):
    for x in range(length):
        try:
            window.set_at((x, y), rendered_screen[y][x])
        except:
            print(rendered_screen[y][x])
pygame.image.save(window, "result.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.update()

pygame.quit()
