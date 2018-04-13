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
diff_const = .2

# Temperate of rod at rest
temp0 = 0

# time delta
k = .01

iterations = 4000
slices = 60

# Known conditions at the edges
# Evenly spaced increments to 50
# x0, h = np.linspace(0,pi, retstep=True)
space, h = np.linspace(0, pi, slices, retstep=True)
t0 = 0

# multiplier r
r = k/(h**2)
# print(r) #various computational debugs
sigma = diff_const * r #CHANGE: replaced hardcode with diff_const

#CHANGE: the build_matrix functions have been reduced by two positions in order to allow boundary conditions to fall outside of the matrix multiplication

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
#CHANGE: this routine applies neumann conditions, commented out for now
#	A[0][0] = 2 + 2*sigma/3 #changed order of operations... this was casting into some kind of strange type
#	A[1][0] = -2/3 * sigma
#	A[-1][-1] = 2 + 2*sigma/3 #same
#	A[-2][-1] = -2/3 * sigma
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

# Compare Heat function
#def u_compare(x,t):
#	return np.exp(-diff_const*t)*np.sin(x)

#CHANGE: start with no heat in the system
def g(x):
	return 0 #math.sin(x) 


def compute_diff(a, b):
	total = 0
	for i in range(len(a)):
		total += abs(a[i] - b[i]) ** 2
	return total

def left_boundary(vector):
	return vector[0]*(4/3) - (1/3)*vector[1]

def right_boundary(vector):
	return vector[-1]*(4/3) - vector[-2]*(1/3) 

x0 = []
for point in space:
	x0.append(g(point))


temp = [x0]
time = [t0]
point_source_temp = [x0]
error_sum = 0
crank_error_sum = 0

A = build_matrix_A()
B = build_matrix_B()
A_inverse = inv(A)
one_vector = np.zeros(slices-2)
point_contribution = .1 #the system is highly sensitive to changes in this value, which sets the size of the step by step point contribution

for i in range(iterations):
	current_point_temp = point_source_temp[i]
	inner_temps = current_point_temp[1:-1]	#cuts down to non-boundary values
	
	# point heat source
	constant_left = 0 #sets constant left boundary value
	constant_right = 0 #sets constant right boundary value
	side_effects = np.zeros(slices - 2) #builds and sets side effects vector
	side_effects[0] = 2*constant_left #these could be set to functions instead
	side_effects[-1] = 2*constant_right
		
	point_heat = A_inverse.dot(B).dot(inner_temps) + A_inverse.dot(sigma*side_effects) #adds the effect of A inverse onto the side effects vector for Dirichlet conditions
	#Add boundary values back to the point_heat list on the left and right
	next_point_heat = np.insert(point_heat,0,constant_left)
	next_point_heat = np.append(next_point_heat, constant_right)
	next_point_heat[int(round(slices/2))] += point_contribution #this is where the point source is added 
	point_source_temp.append(next_point_heat)


	# compare
	#compare_next = u_compare(space, t0)
	#compare_temp.append(compare_next)
	
	time.append(t0)
	t0 += k

#dimension testing

#print("x length" + str(len(temp[1])))
#print("T length" + str(len(point_source_temp[1])))

p = 0
def animate(i):         #The plot shows the temperature evolving with time
    #global p            #at each point x in the rod
    #x = temp[p]            #The ends of the rod are kept at temperature temp0
    #n = compare_temp[p]
    #c = crank_temp[p]
    h = point_source_temp[i]
   # p += 1              #The rod is heated in one spot, then it cools down
    ax1.clear()
    #plt.plot(space, x, color='red', label='Temperature at each x')
   # plt.plot(space, c, color='green', label='Crank Nicolson')
   # plt.plot(space, n, color='blue', label='Implicit Method')
    plt.plot(space, h, color='black', label='Point Heat Source')
    plt.plot(0,0,color='red',label='Elapsed time '+str(round(time[i],2)))
    plt.grid(True)
    plt.ylim([temp0,2.5])
    plt.xlim([0,pi])
    plt.title('Heat equation')
    plt.legend()
    if p == iterations:
    	sys.exit(0)
#Note: the animate command has been modifed to pass i-values to the animate function. the frame skip needs to be changed whenever you change the number of iterations
frame_skip = 3
anim = animation.FuncAnimation(fig,animate,np.arange(1,iterations,frame_skip), interval=100)
plt.show()
