#!/usr/bin/env python
import pygame
from math import atan2, degrees, pi, cos, sin, hypot

pygame.init()

window_w = 800
window_h = 800

white = (255, 255, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)

FPS = 120

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Bacteria and White Blood Cells")
clock = pygame.time.Clock()

bacteria_x = 600
bacteria_y = 500
block_size = 20
jump_size = 2

def create_bacteria():
    pygame.draw.circle(window, cyan, (bacteria_x, bacteria_y), block_size)

def get_angle(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    print("Degrees: " + str(degs))
    return rads

def next_xy(x, y, angle):
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))

def game_loop():

    velocity = [1, 1]

    pos_x = window_w/2
    pos_y = window_h/2

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # check first if we've hit our target
        xcond = pos_x + block_size > bacteria_x
        ycond = pos_y + block_size > bacteria_y
        if xcond and ycond:
            print("Collision found!")
            return

        rads = get_angle(pos_x, pos_y)
        coords = next_xy(pos_x, pos_y, rads)
        print("Coords: " + str(coords))

        pos_x += coords[0] #velocity[0]
        pos_y += coords[1] #velocity[1]
        print("New pos: " + str(pos_x) + ", " + str(pos_y))

        # keep within window
        if pos_x + block_size > window_w or pos_x < 0:
            velocity[0] = -velocity[0]
        if pos_y + block_size > window_h or pos_y < 0:
            velocity[1] = -velocity[1]

        # DRAW
        window.fill(white)
        create_bacteria()
        pygame.draw.circle(window, black, (pos_x, pos_y) , block_size)
        pygame.display.update()
        clock.tick(FPS)

game_loop()