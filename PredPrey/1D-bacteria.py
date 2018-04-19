#!/usr/bin/env python
import pygame
from math import atan2, degrees, pi, cos, sin, hypot, sqrt
from scipy.stats import truncnorm
import random
import numpy as np
from numpy import pi
import sys
import math
from numpy.linalg import inv



window_w = 800
window_h = 800

window = pygame.display.set_mode((window_w, window_h))
block_size = 20

white = (255, 255, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

FPS = 120


# diffusion constant
diff_const = .2

# Temperate of rod at rest
temp0 = 0

# time delta
k = .01

iterations = 4000
slices = 140

# Known conditions at the edges
# Evenly spaced increments to 50
# x0, h = np.linspace(0,pi, retstep=True)
space, h = np.linspace(0, pi, slices, retstep=True)
t0 = 0

# multiplier r
r = k/(h**2)
# print(r) #various computational debugs
sigma = diff_const * r #CHANGE: replaced hardcode with diff_const

def build_matrix_A():
	A = np.zeros((slices-2, slices-2))
	for i in range(slices-2):
		A[i][i] = 2 + 2 * sigma
		try:
			A[i][i+1] = -sigma
		except:
			pass
		try:
			A[i+1][i] = -sigma
		except:
			pass
	return A

def build_matrix_B():
	B = np.zeros((slices-2, slices-2))
        for i in range(slices-2):
                B[i][i] = 2 - 2 * sigma
                try:
                        B[i][i+1] = sigma
                except:
                        pass
		try:
			B[i+1][i] = sigma
		except:
			pass
	return B

def g(x):
	return 0


def compute_diff(a, b):
	total = 0
	for i in range(len(a)):
		total += abs(a[i] - b[i]) ** 2
	return total

def left_boundary(vector):
	return vector[0]*(4/3) - (1/3)*vector[1]

def right_boundary(vector):
	return vector[-1]*(4/3) - vector[-2]*(1/3) 

def within_window(x, y):
    # keep within window
    if x + block_size > 700: # window_w:
    	x = x - block_size
    elif x < 0:
        x = x + block_size
    if y + block_size > window_h:
    	y = y - block_size
    elif y < 0:
        y = y + block_size
    return (x, y)

def create_bacteria(bacteria_x, bacteria_y):
    pygame.draw.circle(window, cyan, (bacteria_x, bacteria_y), block_size)

def create_stink(pos_y, factors): # change this for diffusion equation
	stink_diff = pygame.draw.rect(window, (255,0,0), (100, pos_y-50, 600, 100))
	fill_gradient(window, (255,0,0), factors, stink_diff)

def get_distance(x, y):
    dx = bacteria_x - x
    dy = bacteria_y - y
    return hypot(dx, dy)

def check_collision(x, y, bacteria_x, bacteria_y, block_size):
	return sqrt((x-bacteria_x)**2 + (y-bacteria_y)**2) <= 2*block_size

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def fill_gradient(surface, color, factors, rect):
    factors = factors[int(round(slices/2)):]
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    h = x2-x1
    gradient = (255, 255, 255)
    a, b = color, gradient
    rates = []
    for factor in factors:
        rate = (
            float(b[0]-a[0])/h*factor,
            float(b[1]-a[1])/h*factor,
            float(b[2]-a[2])/h*factor
        )
	rates.append(rate)
    fn_line = pygame.draw.line
    for col in range(x1,x2):
    	rate = rates[int(round(col/70))]
        color = (
            min(max(a[0]+(rate[0]*(col-x1)),0),255),
            min(max(a[1]+(rate[1]*(col-x1)),0),255),
            min(max(a[2]+(rate[2]*(col-x1)),0),255)
        )
        fn_line(surface, color, (col,y1), (col,y2))


def calc_diffusion_round(point_source_temp, i):
	point_contribution = .1
	A = build_matrix_A()
	B = build_matrix_B()
	A_inverse = inv(A)
	current_point_temp = point_source_temp
	inner_temps = current_point_temp[1:-1]	#cuts down to non-boundary values
	
	# point heat source
	constant_left = 0 #sets constant left boundary value
	constant_right = 0 #sets constant right boundary value
	side_effects = np.zeros(slices - 2) #builds and sets side effects vector
	side_effects[0] = 2*constant_left #these could be set to functions instead
	side_effects[-1] = 2*constant_right
		
	point_heat = A_inverse.dot(B).dot(inner_temps) + A_inverse.dot(sigma*side_effects) 
	next_point_heat = np.insert(point_heat,0,constant_left)
	next_point_heat = np.append(next_point_heat, constant_right)
	next_point_heat[int(round(slices/2))] += point_contribution
	return next_point_heat

def next_x(x, factors):
	random_range = 5
	rand = random.randint(-random_range, random_range)
	factors = factors[int(round(slices/2)):]
	idx = min(int(round(x/10)), len(factors)-2)
	x -= (factors[idx] * 10) - rand
	print(x)
	return int(round(x))

def game_loop():
    white_x = 700
    white_y = 400
    bacteria_x = 100
    bacteria_y = 400
    pygame.init()
    pygame.display.set_caption("Bacteria and White Blood Cells")
    clock = pygame.time.Clock()
    x0 = []
    for point in space:
	x0.append(g(point))
    point_source_temp = x0
    diffusion_round = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # check first if we've hit our target
        if check_collision(white_x, white_y, bacteria_x, bacteria_y, block_size):
            print("Collision found!")
            return
            
	point_source_temp = calc_diffusion_round(point_source_temp, diffusion_round)

	# Draw constants
	window.fill(white)
	create_stink(bacteria_y, point_source_temp)
	create_bacteria(bacteria_x, bacteria_y)

	white_x = next_x(white_x, point_source_temp)


	white_x, white_y = within_window(white_x, white_y)
	print("New pos: " + str(white_x) + ", " + str(white_y))
	# DRAW
	pygame.draw.circle(window, black, (white_x, white_y) , block_size)
	pygame.display.update()
        clock.tick(FPS)
	diffusion_round += 1

game_loop()
