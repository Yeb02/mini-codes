import sys
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
import cv2
import time
from mpl_toolkits.mplot3d import Axes3D
from pylab import *




def gol(nbtours, largeur, hauteur):

    u1 = [3, 4, 5]   #nb de voisines pour faire naitre
    u2 = [2, 3, 4, 5, 6]   #nb de voisines pour survivre
    ray = 2       #rayon du cercle d' influence


    grille2 = np.zeros((hauteur, largeur), dtype=int)


    #random:

    for by in range(largeur):
        for cy in range(hauteur):
            grille2[cy, by] = np.random.random_integers(0, 1)


    # grille2[4, 3] = 1
    # grille2[4, 4] = 1
    # grille2[4, 5] = 1
    # grille2[3, 3] = 1
    # grille2[2, 4] = 1


    def ringsum(y, x, grille):
        s = - grille[y, x]
        for b in range(-ray, ray + 1):
            for a in range(-ray, ray + 1):
                s += grille[(y + b) % (hauteur), (x + a) % (largeur)]
        return(s)

    def caprice(u1, u2, s, y, x, grille):
        k = 0
        if grille[y ,x] == 0:
            for elt in u1:
                if s == elt:
                    k = 1
        if grille[y ,x] == 1:
            for elt in u2:
                if s == elt:
                    k = 1
        return(k)


    def tour(grille2):
        grille = grille2
        grille2 = np.zeros((hauteur, largeur), dtype=int)
        for y in range(hauteur):
                for x in range(largeur):
                    s = ringsum(y, x, grille)
                    k = caprice(u1, u2, s, y, x, grille)
                    grille2[y, x] = k
        return(grille2)


    for z in range(nbtours):
        plt.matshow(grille2, fignum=0)
        grille2 = tour(grille2)
        plt.pause(.01)
        plt.clf()


    plt.show()

