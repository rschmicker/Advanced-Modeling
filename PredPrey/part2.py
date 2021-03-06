#!/usr/bin/env python
import pygame
from math import atan2, degrees, pi, cos, sin, hypot, sqrt
from scipy.stats import truncnorm
from numpy import exp
import random
import numpy as np

pygame.init()

window_w = 800
window_h = 800

white = (255, 255, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

FPS = 120

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Bacteria and White Blood Cells")
clock = pygame.time.Clock()

random_range = 5
bacteria_x = 400
bacteria_y = 400
block_size = 20
stink_size = 10
jump_size = 2
k = .05

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def within_window(x, y):
    # keep within window
    if x + block_size > window_w:
    	x = x - block_size
    elif x < 0:
        x = x + block_size
    if y + block_size > window_h:
    	y = y - block_size
    elif y < 0:
        y = y + block_size
    return (x, y)

def create_stink(meshgrid):
    x = 400
    y = 400
    print(100*meshgrid[400])
    for radius in range(400, 0, -1):
	color = (max(min(255, 150 + 100*meshgrid[radius][400]), 0), 0, 0)
        pygame.draw.circle(window, color, (x, y), radius)
    # sys.exit(0)

def create_bacteria():
    global bacteria_x
    global bacteria_y
    #bacteria_x += random.randint(-bacteria_random_range, bacteria_random_range)
    #bacteria_y += random.randint(-bacteria_random_range, bacteria_random_range)
    #bacteria_x, bacteria_y = within_window(bacteria_x, bacteria_y)
    pygame.draw.circle(window, cyan, (bacteria_x, bacteria_y), block_size)

def get_distance(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    return hypot(dx, dy)

def get_std_dev(x, y, mesh, angle):
    distance = mesh[x][y] # get_distance(x, y)
    sigma = k * distance**(.5)
    std = get_truncated_normal(mean=angle, sd=sigma, low=0, upp=2*pi)
    return std.rvs()

def get_angle(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    # print("Degrees: " + str(degs))
    return rads

def p_model(angle):
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))


def model(x, y, angle, mesh):
    angle = get_std_dev(x, y, mesh, angle)
    # print("Std Angle: " + str(degrees(angle)))
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))

def check_collision(x, y):
	return sqrt((x-bacteria_x)**2 + (y-bacteria_y)**2) <= 2*block_size

def inside_stink(x, y):
	return sqrt((x-bacteria_x)**2 + (y-bacteria_y)**2) <= stink_size

# diffusion function
"""
create mesh grird same size as windows height and width
reference the temp grid to determine where to go
max temp from current temp at this cell to swap out for our distance

"""
def diffusion_map(x,y,t):
    time_reverse = 10
    T = 5 # initial temp
    s = 2 # sigma squared
    x = np.linspace(-5,5,800)
    y = np.linspace(-5,5,800)
    x,y = np.meshgrid(x,y)
    return (T/sqrt(1+4*max(time_reverse - t, 0)/s))*exp(-(x**2+y**2)/(s+4*max(time_reverse - t, 0)))

def game_loop():
    pos_x = 700
    pos_y = 700
    perfect_x = 700
    perfect_y = 700
    t0 = 0
    dt = 0.05
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # check first if we've hit our target
        if check_collision(pos_x, pos_y):
            print("Collision found!")
            return

	# Draw constants
	window.fill(white)
	
	diff_map = diffusion_map(bacteria_x, bacteria_y, t0)
	create_stink(diff_map)
	create_bacteria()

	# p_rads = get_angle(perfect_x, perfect_y)
	# p_coords = p_model(p_rads)
	# perfect_x += p_coords[0]
	# perfect_y += p_coords[1]
	# pygame.draw.circle(window, green, (perfect_x, perfect_y), block_size)

	# check if we are now inside the stink
	if 1: # inside_stink(pos_x, pos_y):
	    # get new angle
		rads = get_angle(pos_x, pos_y)
		coords = model(pos_x, pos_y, rads, diff_map)
		pos_x += coords[0] # + random.randint(-random_range, random_range)
		pos_y += coords[1] # + random.randint(-random_range, random_range)
	else:
		pos_x += random.randint(-random_range, random_range)
		pos_y += random.randint(-random_range, random_range)

	pos_x, pos_y = within_window(pos_x, pos_y)
	# print("New pos: " + str(pos_x) + ", " + str(pos_y))
	# DRAW
	pygame.draw.circle(window, black, (pos_x, pos_y) , block_size)
	pygame.display.update()
	clock.tick(FPS)
	t0 += dt

game_loop()
