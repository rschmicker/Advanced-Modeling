#!/usr/bin/env python
import numpy as np
from numpy import pi
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys
import math

fig = plt.figure()
fig.set_dpi(100)
ax1 = fig.add_subplot(1,1,1)

# Heat function
# def u(x,t):
# 	return temp0 + np.exp(-diff_const*t)*np.sin(x)

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

def g(x):
	return math.sin(x)

def u(x, t, current_temps):
	left = current_temps[x - 1]
	right = current_temps[x + 1]
	center = current_temps[x]
	u_next = (1-2*r)*center + r*left + r*right
	return u_next

x0 = []
for point in space:
	x0.append(g(point))

# 2D surface (x,t) -> temperate vs. time
# temperature [0, pi]
# time [0, 10]
temp = [x0]
time = [t0]

for i in range(iterations):
	current_temps = temp[i]
	next_temps = []
	next_temps.append(0) # zero at the edges
	for x in range(1, len(current_temps) - 1):
		u_next = u(x, t0, current_temps)
		next_temps.append(u_next)
	next_temps.append(0) # zero at the edges
	temp.append(next_temps)
	time.append(t0)
	t0 += k

p = 0
def animate(i):         #The plot shows the temperature evolving with time
    global p            #at each point x in the rod
    x = temp[p]            #The ends of the rod are kept at temperature temp0
    p += 1              #The rod is heated in one spot, then it cools down
    ax1.clear()
    plt.plot(space,x,color='red',label='Temperature at each x')
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

