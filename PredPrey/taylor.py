#!/usr/bin/env python
import plotly
import plotly.graph_objs as go

# u(x+h) = u(x) + h(u'(x))

def func(x):
	return 3 * x + 2

def main():
	h = 0.333333333
	xs = []
	ys = []
	ux = 1
	x_pos = 0
	for x in range(3):
		x_pos = x_pos + h
		xs.append(x_pos)
		y_pos = ux + h*(func(ux))
		ys.append(y_pos)
		ux = y_pos
		print("x: " + str(x_pos) + " y: " + str(y_pos))

	trace = go.Scatter(
		x = xs,
		y = ys,
		#mode = 'markers'
	)

	data = [trace]
	plot_url = plotly.offline.plot(data, filename='basic-line.html')

main()