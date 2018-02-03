#!/usr/bin/env python
import pygame
from math import atan2, degrees, pi, cos, sin, hypot, sqrt
from scipy.stats import truncnorm
import random

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

bacteria_random_range = 5
bacteria_x = 200
bacteria_y = 100
block_size = 20
jump_size = 2
k = 500

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def within_window(x, y):
    # keep within window
    if x + block_size > window_w or x < 0:
        x = -x
    if y + block_size > window_h or y < 0:
        y = -y
    return (x, y)

def create_bacteria():
    global bacteria_x
    global bacteria_y
    bacteria_x += random.randint(-bacteria_random_range, bacteria_random_range)
    bacteria_y += random.randint(-bacteria_random_range, bacteria_random_range)
    bacteria_x, bacteria_y = within_window(bacteria_x, bacteria_y)
    pygame.draw.circle(window, cyan, (bacteria_x, bacteria_y), block_size)

def get_distance(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    return hypot(dx, dy)

def get_std_dev(x, y, angle):
    distance = get_distance(x, y)
    sigma = k / distance
    std = get_truncated_normal(mean=angle, sd=sigma, low=0, upp=2*pi)
    return std.rvs()

def get_angle(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    print("Degrees: " + str(degs))
    return rads

def next_xy(x, y, angle):
    angle = get_std_dev(x, y, angle)
    print("Std Angle: " + str(degrees(angle)))
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))

def game_loop():
    pos_x = 700
    pos_y = 700

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # check first if we've hit our target
        cond = sqrt((pos_x-bacteria_x)**2 + (pos_y-bacteria_y)**2) <= 2*block_size
        if cond:
            print("Collision found!")
            return

        # get new angle
        rads = get_angle(pos_x, pos_y)
        coords = next_xy(pos_x, pos_y, rads)

        pos_x += coords[0]
        pos_y += coords[1]
        pos_x, pos_y = within_window(pos_x, pos_y)
        print("New pos: " + str(pos_x) + ", " + str(pos_y))

        # DRAW
        window.fill(white)
        create_bacteria()
        pygame.draw.circle(window, black, (pos_x, pos_y) , block_size)
        pygame.display.update()
        clock.tick(FPS)

game_loop()