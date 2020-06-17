import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import noise
from numpy import cos, sin, sqrt
import random
import itertools



def epicentre(n, p, seuil, col):
    cpt = 0
    while True:
        t = 0
        g, speed = grille_perlin(n, p, seuil)
        theta = 0
        r = int(n/8)
        perimetre = int(3*np.pi*r)
        for k in range(0, perimetre, 3):
            theta = 2 * np.pi * k/r
            x = int(r * cos(theta)) + int(n/2)
            y = int(r * sin(theta)) + int(n/2)
            if g[x][y] == 0:
                thetabase = theta
                t = 1
            elif g[x][y] == 1:
                t = 0
            if g[x][y] == 0 and t == 1 and g[int(r * cos((theta + thetabase)/2)) + int(n/2), int(r * sin((theta + thetabase)/2)) + int(n/2)] == 0:
                x = int(r * cos((theta + thetabase)/2)) + int(n/2)
                y = int(r * sin((theta + thetabase)/2)) + int(n/2)
                g[x][y] = 1
                premierfront = []
                v = speed[x, y]
                theta = 0
                peri = int(3*np.pi*v)
                for i in range(peri):
                    d = 1  #sqrt(2)
                    while 0 < x + int(d*cos(theta)) < n and 0 < y + int(d*sin(theta)) < n and d < v:
                        if g[x + int(d*cos(theta))][y + int(d*sin(theta))] == 0:
                            g[x + int(d*cos(theta))][y + int(d*sin(theta))] = col
                        d += 1
                    if d > 1:
                        d -= 1
                        premierfront.append([x + int(d*cos(theta)), y + int(d*sin(theta)), theta])
                    theta += 2*np.pi/peri

                return speed, premierfront, g
        cpt += 1
        print('choix de r trop petit dans la fct epicentre, ou PAS DE CHANCE, iteration numéro:', cpt)



def front_spherique(n, p, seuil, phi):    #seuil doit valoir 1.5*n environ, p entre 0 et 1, phi est l'angle de propag.
    random.seed(1)
    col = 20 #couleur de l'épicentre, faire commencer à env. 20 pour distinguer des zones jamais atteintes ?
    speed, front, g = epicentre(n, p, seuil, col)     #et doit valoir environ 0. (C'est selon, empiriquement.)
    k = col
    cst = 1.2
    while front != []:
        k += 20   #plus pour rendre significatives les avancées
        if k%1 == 0:  #affichage tout les 1 iter
            plt.clf()
            afficher_couleur_bis(g, speed)    #extremement rapide sans l' affichage, mettre en plein écran fait lager.
            plt.pause(.01)
        frontbis = []
        for elt in front:
            cox, coy = elt[0], elt[1]    #le + 1 est arbitraire, c'est pour éviter que l'onde s' arrête totalement
            v = speed[cox, coy] + 1     #dans les hauts-fonds.
            theta = elt[2] - phi
            peri = int(v*phi*3)  #nb de cases à distance v sur un angle 2*phi
            for i in range(peri):
                d = cst  #sqrt(2) ?
                while 0 < cox + int(d*cos(theta)) < n and 0 < coy + int(d*sin(theta)) < n and d < v:
                    if g[cox + int(d*cos(theta))][coy + int(d*sin(theta))] == 0:
                        g[cox + int(d*cos(theta))][coy + int(d*sin(theta))] = k
                    d += cst
                if d > cst and (i%(1 + int(peri/2)) == 0 or i == peri - 1) and 0 < cox + int(d*cos(theta)) < n and 0 < coy + int(d*sin(theta)) < n and g[cox + int(d*cos(theta))][coy + int(d*sin(theta))] == 0:
                    #prendre une fraction(1/3, 1/10 des elts ? de l'ordre de 1/vitessemoyenne)
                    frontbis.append([cox + int(d*cos(theta)), coy + int(d*sin(theta)), theta])
                theta += 2*phi/peri

        frontbis.sort()
        l = len(frontbis)
        front = []
        elt1 = frontbis[0]
        elt2 = frontbis[1]
        if elt2[2] > elt1[2]:
            front.append(elt2)
            front.append(elt1)
        else:
            front.append(elt1)
            front.append(elt2)
        for (i, elt1) in enumerate(frontbis):   #mal optimisé
            if [front[-1][0], front[-1][1]] != [elt1[0], elt1[1]]:
                if i + 1 < l:
                    elt2 = frontbis[i + 1]
                    if elt2[2] > elt1[2]:
                        front.append(elt2)
                        front.append(elt1)
                    else:
                        front.append(elt1)
                        front.append(elt2)
                else:
                    front.append(elt1)
            elif elt1[2] < front[-1][2]:
                front[-1] = elt1
            elif elt1[2] > front[-2][2]:
                front[-2] = elt1


        # front = list(frontbis for frontbis,_ in itertools.groupby(frontbis)) #enleve les doublons

        # front = []
        # front1 = list(frontbis for frontbis,_ in itertools.groupby(frontbis))
        # for elt in front1:
        #     if g[elt[0], elt[1]] == 0:
        #         front.append(elt)

        print(len(frontbis), len(front))
    print('done building')
    afficher_couleur_bis(g, speed)

def afficher_couleur_bis(G, s):
    plt.subplot(121)
    plt.imshow(G, cmap='jet')  #'binary' pour noir et blanc; 'jet' pour le spectre. (où est passé spectral ?)
    plt.subplot(122)
    plt.imshow(s, cmap='jet')
    plt.show()


def grille_perlin(n, p, seuil):
    depthmax = 5   #fct de n, ici si n = 200 les profondeurs varient
    g = np.zeros([n, n])
    depth = np.zeros([n, n])
    scale = n * 1/2   #zoom, fct croissante, 1/12 et 1/5 interessant (1/5 pour continent)
    b = int(100 * rd.random())
    for i in range(n):
        for j in range(n):
            pernoise = noise.pnoise2(i/scale,
                                        j/scale,
                                        octaves=10,
                                        persistence=.35, #.5 de base, taille des blocs (fct croissante), .35 ?
                                        lacunarity=2,   #2 de base, nb de petits trous(plus si plus grand)
                                        repeatx=n,
                                        repeaty=n,
                                        base=b)
            g[i][j] = (.05 + pernoise - (1 - p)/5 < 0) * seuil             #à bidouiller
            depth[i][j] = (.05 + pernoise - (1 - p)/5 > 0) * pernoise
    depth = 1 - np.exp(-5 * depth)
    min = np.amin(depth)
    speed = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            if depth[i, j] != 0:
                speed[i, j] = np.sqrt((depth[i, j] - min) * depthmax * 9.81)
    return(g, speed)