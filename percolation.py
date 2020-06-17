import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import noise
from numpy import cos, sin, sqrt
import random
import itertools

from matplotlib.colors import ListedColormap
echelle = ListedColormap(['black', 'aqua', 'white'])

#### basique

def grille(p, n):
    G = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            G[i, j] = rd.random() < p
    return G
            
def afficher(G):
    plt.imshow(G, cmap = echelle)
    plt.show()      
    
def remplir_ligne1(G):    
    for j in range(len(G)):
        if G[0, j] == 1:
            G[0, j] = 0.5
  

        
def explorer(g, cox, coy):
    plt.clf()
    afficher(g)
    plt.pause(.1)
    g[cox, coy] = .5
    if 0 <= cox + 1 < n and g[cox + 1, coy] == 1:
        g = explorer(g, cox + 1, coy)
    if 0 <= cox - 1 < n and g[cox - 1, coy] == 1:
        g = explorer(g, cox - 1, coy)
    if 0 <= coy - 1 < n and g[cox, coy - 1] == 1:
        g = explorer(g, cox, coy - 1)
    if 0 <= coy + 1 < n and g[cox, coy + 1] == 1:
        g = explorer(g, cox, coy + 1)
    # afficher(g)
    # plt.pause(.01)
    # plt.clf()
    return(g)

    

def init(G):    
    for j in range(len(G)):
        if G[0, j] == 1:
            G[0, j] = 0.5
            return(G, j)
    return(G, 0)

def recursif(n1, p):
    global n
    n = n1
    g = grille(p, n)
    g, coy = init(g)
    cox = 0
    g = explorer(g, cox, coy)
    afficher(g)


def recursif_ligne(n1, p):
    global n
    n = n1
    g = grille(p, n)
    remplir_ligne1(g)
    
    for k in range(n):
        if g[0, k] == .5:
            g = explorer(g, 0, k)
    afficher(g)

########  récursif coloré

def init_couleur(G):    
    for j in range(len(G)):
        if G[0, j] == -1:
            G[0, j] = 0
            return(G, j)
    return(G, 0)

def grille_couleur(n, p, seuil):
    G = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            G[i, j] = (rd.random() < (1 - p)) * seuil
    return(G)

def explorer_couleur(g, cox, coy, d):
    # plt.clf()
    # afficher_couleur(g)
    # plt.pause(.01)
    g[cox, coy] = d
    if 0 <= cox + 1 < n and g[cox + 1, coy] == 0:
        g = explorer_couleur(g, cox + 1, coy, d + 1)
    if 0 <= cox - 1 < n and g[cox - 1, coy] == 0:
        g = explorer_couleur(g, cox - 1, coy, d + 1)
    if 0 <= coy - 1 < n and g[cox, coy - 1] == 0:
        g = explorer_couleur(g, cox, coy - 1, d + 1)
    if 0 <= coy + 1 < n and g[cox, coy + 1] == 0:
        g = explorer_couleur(g, cox, coy + 1, d + 1)
    return(g)


def recursif_couleur(n1, p, seuil):  #seuil en n*ln(n) ?
    global n
    n = n1
    g = grille_couleur(n, p, seuil)
    g, coy = init_couleur(g)
    cox = 0
    g = explorer_couleur(g, cox, coy, 1)
    afficher_couleur(g)
    
def afficher_couleur(G):
    plt.imshow(G, cmap='jet')  #'binary' pour noir et blanc; 'jet' pour le spectre. (où est passé spectral ?)
    plt.show()
    
    
#######    Grille de perlin

def front_ligne_1(g):
    front = []
    for j in range(len(g)):
        if g[0, j] == 0:
            g[0, j] = 1
            front.append([0, j])
    return(front, g)

def front_couleur(n, p, seuil):  #seuil en n, p à l'infini. Quelle fonction ? pour des petites valeurs prendre du 2 ou 3 n
    # g = grille_couleur(n, p, seuil)   #version moins interessante
    g, _ = grille_perlin(n, p, seuil)   #version interessante
    front, g = front_ligne_1(g)
    k = 1   
    # k = int(seuil/10) + 1  #commencer avec un seuil pour distinguer le début des inatteignables, peut entrer en 
    while front != []:     #  conflit avec les estimations de seuil(n)
        k += 1
        plt.clf()
        afficher_couleur(g)    #extremement rapide sans l' affichage, mettre en plein écran fait lager.
        plt.pause(.01)
        frontbis = []
        for elt in front:   #○tres mal optimisé, 2 voire 4 fois trop de comparaisons
            cox, coy = elt[0], elt[1]
            if 0 <= cox + 1 < n and g[cox + 1, coy] == 0:
                g[cox + 1, coy] = k
                frontbis.append([cox + 1, coy])
            if 0 <= cox - 1 < n and g[cox - 1, coy] == 0:
                g[cox - 1, coy] = k
                frontbis.append([cox - 1, coy])
            if 0 <= coy - 1 < n and g[cox, coy - 1] == 0:
                g[cox, coy - 1] = k
                frontbis.append([cox, coy - 1])
            if 0 <= coy + 1 < n and g[cox, coy + 1] == 0:
                g[cox, coy + 1] = k
                frontbis.append([cox, coy + 1])
        front = list(frontbis)
    print('done building')
    #on pourrait facilement automatiser le seuil pour le rendu final mais laborieusement pour le film
    afficher_couleur(g)

    
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