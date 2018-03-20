#!/usr/bin/env python

import numpy as np

equation_constants = np.array([[2, -3, 1], [1, -2, 5], [3, 3, -10]])
equals = np.array([6, 1, 2])

solve = np.linalg.solve(equation_constants, equals)
print(solve)