import sys
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
import cv2
import time
from mpl_toolkits.mplot3d import Axes3D
from pylab import *



def mandelbrot(defv, defh): #100, 100 basse def, 1000 1000 ok.
    xmin = -2
    xmax = .5
    ymin = -1
    ymax = 1

    fig, ax = plt.subplots()

    # xmin = -.0396
    # xmax = -.161
    # ymax = .7721
    # ymin = .55


    xlim(xmin, xmax)
    ylim(ymin, ymax)

    ux = []
    uy = []
    col = []

    def mand(e, f):
        c = x[f] + y[e]*1j
        z0 = 0
        a = 0
        while a < 60:  #à étudier
            z0 = z0 ** 2 + c
            a += 1
            if abs(z0) > 2:
                a = 100
        if a != 100:
            ux.append(x[f])
            uy.append(y[e])


    x = np.linspace(xmin, xmax, defh + 1)
    y = np.linspace(ymin, ymax, defv + 1)

    for e in range(defv + 1):
        print(e)
        for f in range(defh + 1):
            mand(e, f)
    plt.plot(ux, uy, 'bo', markersize = 0.6)


    # xlim(xmin, xmax)
    # ylim(ymin, ymax)
    # col = []
    # x = np.linspace(xmin, xmax, defh + 1)
    # y = np.linspace(ymin, ymax, defv + 1)
    #
    # for e in range(defv + 1):
    #     print(e)
    #     for f in range(defh + 1):
    #         c = x[f] + y[e]*1j
    #         z0 = 0
    #         a = 0
    #         while a < 60:  #à étudier
    #             z0 = z0 ** 2 + c
    #             a += 1
    #             if abs(z0) > 2:
    #                 a = 100
    #         if a != 100:
    #             col = '{}'.format(abs(z0)/2)
    #             ax.scatter(x[f], y[e], c=col)

    plt.show()