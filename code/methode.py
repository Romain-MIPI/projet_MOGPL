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
        
def construction_arboresecnce(graphe, dist, pred):
    """Construit l'arborescence des PCCH"""
    sommets, arcs = graphe
    newA = []
    for i in range(len(sommets)):
        if dist[i] != 0:
            for (u, v, c) in arcs:
                if u == pred[i] and v == sommets[i]:
                    newA.append((u, v, c))
                    continue
    return (sommets, newA)

def bellman_Ford(graphe):
    """Algo Bellman-Ford appliqué pour le graphe
    entrée:
        graphe : tuple(liste d'ordre de sommets, liste d'arcs)
    sortie:
        tuple(arborescence de PCCH, nombre d'itérations)
    """
    #src=source(graphe)
    sommets, arcs = graphe
    src = sommets[0]
    dist = [[float(math.inf)] * len(sommets), [float(math.inf)] * len(sommets)] #matrice de distance, stoque que dist[k] et dist[k+1] à chaque itération
    pred = [None] * len(sommets)    #liste de sommet prédecesseur
    dist[0][sommets.index(src)] = 0
    dist[1][sommets.index(src)] = 0
    
    for i in range(0, len(sommets)):
        for (u,v,w) in arcs:
            indu, indv = sommets.index(u), sommets.index(v)
            if dist[i%2][indu]+w < dist[i%2][indv]: #i%2 <- k, (i+1)%2 <- k+1
                dist[(i+1)%2][indv]=dist[i%2][indu]+w
                pred[indv] = u

        #print("dist =", dist)
        #print("pred =", pred)

        if dist[i%2] == dist[(i+1)%2]:  #si convergence
            return construction_arboresecnce(graphe, dist[(i+1)%2], pred), i+1
        dist[i%2] = [dist[(i+1)%2][j] for j in range(len(sommets))]

    #Bellman-Ford doit convergé à au plus n-1 itérztions s'il n'a pas de cycle absorbant
    raise NameError("non convergence, il existe un cycle absorbant")

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

def genere_graphe(nb_sommets,p):
    g=[]
    list_sommets=[i for i in range(nb_sommets)]
    while(True):
        list_weight=[np.random.randint(-10,11) for _ in range(4)]
        list_arc=[(i,j,np.random.choice(list_weight)) for i in range(nb_sommets) for j in range(nb_sommets) if np.random.random()<p and i!=j]
        g=list_sommets,list_arc
        if not(check_circuit_negatif(g)):
            break



    return g

def check_circuit_negatif(graphe):
    list_sommets,list_arc=graphe
    A=np.zeros((len(list_sommets),len(list_sommets)))

    for i in range(len(list_sommets)):
        for j in range(len(list_sommets)):
            if i!=j:
                A[(i,j)]=float(math.inf)

    for arc in list_arc:
        A[arc[0]][arc[1]]=arc[2]


    for _ in range(len(list_sommets)):
        for i in range(len(A)):
            for j in range(len(A[i])):
                for k in range(len(list_sommets)):
                    A[(i,j)]=min(A[(i,j)],A[(i,k)]+A[(k,j)])

    
    for i in range(len(A)):
        if A[(i,i)]!=0:
            return True #Circuit detecté
        
    return False #NO CIRCUIT
