from scipy.optimize import fsolve
from math import log

import pandas as pd
import matplotlib.pyplot as plt

pp = 0.2

k = {}
P = []

for i in xrange(1, 116):
    k[i] = i+5
    P.append(0)


def func(P):
    global pp
    global k
    return log(1-pp)-(2*P-2*k[i]+1)*log(1-k[i]/P)+(P-2*k[i]+0.5)*log(1-2*k[i]/P)

def plotData(plt, data):
  x = [p[0] for p in data]
  y = [p[1] for p in data]
  plt.plot(x, y, '-o')

for i in xrange(1, 121):
    gP =  -k[i]**2/log(1-pp)
    P[i-1] = (i, fsolve(func, gP)[0])

plotData(plt, P)

pp = 0.5
for i in xrange(1, 121):
    gP =  -k[i]**2/log(1-pp)
    P[i-1] = (i, fsolve(func, gP)[0])

plotData(plt, P)

pp = 0.8
for i in xrange(1, 121):
    gP =  -k[i]**2/log(1-pp)
    P[i-1] = (i, fsolve(func, gP)[0])

plotData(plt, P)

plt.show()
