#!/usr/bin/env python
import numpy as np
from numpy import pi
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys
import math
from numpy.linalg import inv

fig = plt.figure()
fig.set_dpi(100)
ax1 = fig.add_subplot(1,1,1)

# diffusion constant
diff_const = 2

# Temperate of rod at rest
temp0 = 0

# time delta
k = 0.01

iterations = 500
slices = 20

# Known conditions at the edges
# Evenly spaced increments to 50
# x0, h = np.linspace(0,pi, retstep=True)
space, h = np.linspace(0, pi, slices, retstep=True)
t0 = 0

# multiplier r
r = k/(h**2)
sigma = 2 * r

def build_matrix_A():
	A = np.zeros((slices, slices))
	for i in range(slices):
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
	B = np.zeros((slices, slices))
        for i in range(slices):
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

# Compare Heat function
def u_compare(x,t):
	return np.exp(-diff_const*t)*np.sin(x)

def g(x):
	return math.sin(x)

def u(x, t, current_temps):
	left = current_temps[x - 1]
	right = current_temps[x + 1]
	center = current_temps[x]
	u_next = (1-2*r)*center + r*left + r*right
	return u_next

def compute_diff(a, b):
	total = 0
	for i in range(len(a)):
		total += abs(a[i] - b[i]) ** 2
	return total

x0 = []
for point in space:
	x0.append(g(point))

# 2D surface (x,t) -> temperate vs. time
# temperature [0, pi]
# time [0, 10]
temp = [x0]
time = [t0]
compare_temp = []
crank_temp = []
point_source_temp = []

error_sum = 0
crank_error_sum = 0

A = build_matrix_A()
B = build_matrix_B()
A_inverse = inv(A)
one_vector = np.zeros(slices)
one_vector[int(slices/2)] = 1

for i in range(iterations):
	current_temps = temp[i]
	
	# crank nicolson
	next_crank = A_inverse.dot(B).dot(current_temps)
	crank_temp.append(next_crank)

	# point heat source
	next_point_heat = np.add(A_inverse.dot(B).dot(current_temps), A_inverse.dot(one_vector))
	point_source_temp.append(next_point_heat)

	# implicit
	next_temps = []
	next_temps.append(0) # zero at the edges
	for x in range(1, len(current_temps) - 1):
		u_next = u(x, t0, current_temps)
		next_temps.append(u_next)

	# compare
	compare_next = u_compare(space, t0)
	compare_temp.append(compare_next)
	
	next_temps.append(0) # zero at the edges
	error_sum += compute_diff(next_temps, compare_next)
	crank_error_sum += compute_diff(next_crank, compare_next)
	temp.append(next_temps)
	time.append(t0)
	t0 += k

print("Implicit error: " + str(math.sqrt(float(error_sum))))
print("Crank Nicolson error: " + str(math.sqrt(float(crank_error_sum))))

p = 0
def animate(i):         #The plot shows the temperature evolving with time
    global p            #at each point x in the rod
    x = temp[p]            #The ends of the rod are kept at temperature temp0
    n = compare_temp[p]
    c = crank_temp[p]
    h = point_source_temp[p]
    p += 1              #The rod is heated in one spot, then it cools down
    ax1.clear()
    plt.plot(space, x, color='red', label='Temperature at each x')
    plt.plot(space, c, color='green', label='Crank Nicolson')
    plt.plot(space, n, color='blue', label='Implicit Method')
    plt.plot(space, h, color='black', label='Point Heat Source')
    plt.plot(0,0,color='red',label='Elapsed time '+str(round(time[p],2)))
    plt.grid(True)
    plt.ylim([temp0,2.5])
    plt.xlim([0,pi])
    plt.title('Heat equation')
    plt.legend()
    if p == iterations:
    	sys.exit(0)
anim = animation.FuncAnimation(fig,animate,frames=360,interval=200)
plt.show()

