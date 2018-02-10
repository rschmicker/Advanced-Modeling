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
red = (255, 0, 0)
green = (0, 255, 0)

FPS = 120

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Bacteria and White Blood Cells")
clock = pygame.time.Clock()

random_range = 5
bacteria_x = 200
bacteria_y = 100
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

def create_stink():
	global bacteria_x
	global bacteria_y
	global stink_size
	pygame.draw.circle(window, red, (bacteria_x, bacteria_y), stink_size)
	stink_size += 1

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

def get_std_dev(x, y, angle):
    distance = get_distance(x, y)
    sigma = k * distance**(.5)
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

def p_model(angle):
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))


def model(x, y, angle):
    angle = get_std_dev(x, y, angle)
    print("Std Angle: " + str(degrees(angle)))
    next_x = jump_size * cos(angle)
    next_y = jump_size * sin(angle)
    return (int(next_x), int(-next_y))

def check_collision(x, y):
	return sqrt((x-bacteria_x)**2 + (y-bacteria_y)**2) <= 2*block_size

def inside_stink(x, y):
	return sqrt((x-bacteria_x)**2 + (y-bacteria_y)**2) <= stink_size

def game_loop():
    pos_x = 700
    pos_y = 700
    perfect_x = 700
    perfect_y = 700

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
	create_stink()
	create_bacteria()

	p_rads = get_angle(perfect_x, perfect_y)
	p_coords = p_model(p_rads)
	perfect_x += p_coords[0]
	perfect_y += p_coords[1]
	pygame.draw.circle(window, green, (perfect_x, perfect_y), block_size)

	# check if we are now inside the stink
	if inside_stink(pos_x, pos_y):
		# get new angle
        	rads = get_angle(pos_x, pos_y)
        	coords = model(pos_x, pos_y, rads)
        	pos_x += coords[0]
        	pos_y += coords[1]
        else:
    		pos_x += random.randint(-random_range, random_range)
    		pos_y += random.randint(-random_range, random_range)

        pos_x, pos_y = within_window(pos_x, pos_y)
        print("New pos: " + str(pos_x) + ", " + str(pos_y))
        # DRAW
        pygame.draw.circle(window, black, (pos_x, pos_y) , block_size)
	pygame.display.update()
        clock.tick(FPS)

game_loop()
