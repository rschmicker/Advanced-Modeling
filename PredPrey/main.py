#!/usr/bin/env python

import Tkinter as tk
from math import atan2, degrees, pi, cos, sin, hypot
import time

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600, borderwidth=0, highlightthickness=0, bg="white")
canvas.grid()

x1 = 0
y1 = 0
x2 = 500
y2 = 500
size = 5
distance = 50
done = False

def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = create_circle

blood_cell = canvas.create_circle(x1, y1, size, fill="red")
bacteria = canvas.create_circle(x2, y2, size, fill="green")
bacteria_coords = canvas.coords(bacteria)

def move_circle(x, y):
	global distance
	dx = x2 - x
	dy = y2 - y
	if hypot(dx, dy) == 0:
		canvas.tag_raise(blood_cell)
		print("bacteria destroyed!")
		return
	if hypot(dx, dy) < distance:
		distance = hypot(dx, dy)
	print("hypot: " + str(hypot(dx, dy)))
	rads = atan2(-dy, dx)
	rads %= 2 * pi
	degs = degrees(rads)
	print("Angle: " + str(degs))
	new_x = distance * cos(rads)
	new_y = abs(distance * sin(rads))
	print("New x: " + str(new_x) + " New Y: " + str(new_y))
	canvas.move(blood_cell, new_x, new_y)
	canvas.after(1 * 1000, move_circle, new_x + x, new_y + y)

def main():
	root.wm_title("Bacteria and White Blood Cells")
	move_circle(x1, y1)
	root.mainloop()

main()