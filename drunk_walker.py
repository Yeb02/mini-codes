import sys
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
import cv2
import time
from mpl_toolkits.mplot3d import Axes3D
from pylab import *


def marche_aleatoire_2D(n):
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    x, y = 0, 0
    pgauche = .5
    phaut = .5
    for a in range(n):
        dx, dy = 0, 0
        u = uniform(0, 2)
        if u < pgauche:
            dx -= 1
        elif u < 1:
            dx += 1
        elif u < 1 + phaut:
            dy += 1
        else:
            dy -= 1
        plt.plot((x, x+dx), (y, y+dy), color='red', alpha = .3)
        x += dx
        y += dy
        plt.pause(.01)
    plt.show()

def marche_aleatoire_3D(n):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = 0, 0, 0
    pgauche = .5
    phaut = .5
    pfond = .5
    lim = 20
    ax.set_zlim3d(-lim, lim)
    ax.set_ylim3d(-lim, lim)
    ax.set_xlim3d(-lim, lim)
    ax.set_axis_off()
    for a in range(n):
        dx, dy, dz = 0, 0, 0
        u = uniform(0, 3)
        if u < pgauche:
            dx -= 1
        elif u < 1:
            dx += 1
        elif u < 1 + phaut:
            dy += 1
        elif u < 2:
            dy -= 1
        elif u < 2 + pfond:
            dz += 1
        else:
            dz -= 1
        co = 1 + abs(x) + abs(y) + abs(z)
        # co = lim

        ax.plot([x, x+dx], [y, y+dy], [z, z+dz], color=[abs(x)/co, abs(y)/co, abs(z)/co], alpha = .5)

        ax.view_init(elev=10., azim=2 * a)

        x += dx
        y += dy
        z += dz
        plt.pause(.02)
    plt.show()