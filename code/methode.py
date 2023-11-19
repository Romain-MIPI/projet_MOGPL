import numpy as np
import math
import copy

def source(graphe):
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (_,v,_) in gr_copy[1]:
        if v in list_noeuds:
            list_noeuds.remove(v)
   
    if len(list_noeuds)>=1:
        return list_noeuds[0]
    
    if len(list_noeuds)==0:
        gr_copy=copy.deepcopy(graphe)
        list_entr_sort={key:0 for key in gr_copy[0]}
        for (u,v,_) in gr_copy[1]:
            list_entr_sort[u]+=1
            list_entr_sort[v]-=1
        
        return max(list_entr_sort,key=list_entr_sort.get)
        


def bellman_Ford(graphe):
    """Algo Bellman-Ford appliqué pour le graphe"""
    src=source(graphe)
    dist=[float(math.inf)] * len(graphe[0])
    dist[src]=0
    etat_conv=-1
    
    for i in range(len(graphe[0])):
        conv=True
        for (u,v,w) in graphe[1]:
            if dist[u]+w<dist[v] and dist[u] != math.inf:
                dist[v]=dist[u]+w
                conv = False
        if conv:
            etat_conv=i


    return dist,etat_conv

def list_source(graphe):
    """Vérification si u est la source du graphe"""
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (_,v,_) in gr_copy[1]:
        if v in list_noeuds:
            list_noeuds.remove(v)

    return list_noeuds

def list_puit(graphe):
    """Vérification si u est la source du graphe"""
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (u,_,_) in gr_copy[1]:
        if u in list_noeuds:
            list_noeuds.remove(u)

    return list_noeuds
def supprimer_graphe(u,graphe):
    """Suppression d'un sommet de graphe"""
    graphe[0].remove(u)
    list_arc=copy.deepcopy(graphe[1])
    for (s,v,w) in list_arc:
        if s==u or v==u :
            graphe[1].remove((s,v,w))

    
def gloutonFas(graphe):
    """Algorithme de Glouton Fas"""
    graphe_copy=copy.deepcopy(graphe)
    s1=[]
    s2=[]
    while(graphe_copy[0] != []):
        liste_source=list_source(graphe_copy)
        while(liste_source != []):
            for s in liste_source:
                s1=s1+[s]
                supprimer_graphe(s,graphe_copy)
            liste_source=list_source(graphe_copy)
        
        liste_puits=list_puit(graphe_copy)
        while(liste_puits!=[]):
            for p in liste_puits:
                s2=[p]+s2
                supprimer_graphe(p,graphe_copy)
            liste_puits=list_puit(graphe_copy)
        

        
        if(graphe_copy[0]!=[]):
            u=source(graphe_copy)
            s1=s1+[u]
            supprimer_graphe(u,graphe_copy)
        

    return s1+s2