import numpy as np
import math
import copy
import matplotlib.pyplot as plt

def source(graphe):
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (_,v) in gr_copy[1]:
        if v in list_noeuds:
            list_noeuds.remove(v)
   
    if len(list_noeuds)>=1:
        return list_noeuds[0]
    
    if len(list_noeuds)==0:
        gr_copy=copy.deepcopy(graphe)
        list_entr_sort={key:0 for key in gr_copy[0]}
        for (u,v) in gr_copy[1]:
            list_entr_sort[u]+=1
            list_entr_sort[v]-=1
        
        return max(list_entr_sort,key=list_entr_sort.get)
        
def construction_arboresecnce(graphe, src, pred):
    """Construit l'arborescence des PCCH"""
    sommets, arcs, _ = graphe
    newA = []
    for i in range(len(sommets)):
        if sommets[i] != src:
            for j in range(len(arcs)):
                if arcs[j] == (pred[i], sommets[i]):
                    newA.append(arcs[j])
                    break
    return newA

def bellman_Ford(graphe):
    """Algo Bellman-Ford appliqué pour le graphe
    entrée:
        graphe : tuple(liste d'ordre de sommets, liste d'arcs, liste de poids associé à chaque arc)
    sortie:
        tuple(liste de distance calculée, arborescence de PCCH, nombre d'itérations)
    """
    #src=source(graphe)
    sommets, arcs, poids = graphe
    src = sommets[0]
    dist = [[np.inf] * len(sommets), [np.inf] * len(sommets)] #matrice de distance, stoque que dist[k] et dist[k+1] à chaque itération
    pred = [None] * len(sommets)    #liste de sommet prédecesseur
    dist[0][sommets.index(src)] = 0
    dist[1][sommets.index(src)] = 0
    
    for i in range(0, len(sommets)):
        for j in range(len(arcs)):
            u, v = arcs[j]
            w = poids[j]
            indu, indv = sommets.index(u), sommets.index(v)
            if dist[i%2][indu]+w < dist[i%2][indv]: #i%2 <- k, (i+1)%2 <- k+1
                dist[(i+1)%2][indv]=dist[i%2][indu]+w
                pred[indv] = u

        #print("dist =", dist)
        #print("pred =", pred)

        if dist[i%2] == dist[(i+1)%2]:  #si convergence
            return dist[i%2], construction_arboresecnce(graphe, src, pred), i+1
        
        dist[i%2] = [dist[(i+1)%2][j] for j in range(len(sommets))]

    #Bellman-Ford doit convergé à au plus n-1 itérations s'il n'a pas de cycle absorbant
    #print("non convergence, il existe un cycle absorbant")
    return False

def list_source(graphe):
    """Vérification si u est la source du graphe"""
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (_,v) in gr_copy[1]:
        if v in list_noeuds:
            list_noeuds.remove(v)

    return list_noeuds

def list_puit(graphe):
    """Vérification si u est la source du graphe"""
    gr_copy=copy.deepcopy(graphe)
    list_noeuds=gr_copy[0]

    for (u,_) in gr_copy[1]:
        if u in list_noeuds:
            list_noeuds.remove(u)

    return list_noeuds

def supprimer_graphe(u,graphe):
    """Suppression d'un sommet de graphe"""
    graphe[0].remove(u)
    list_arc=copy.deepcopy(graphe[1])
    for (s,v) in list_arc:
        if s==u or v==u :
            graphe[1].remove((s,v))
    
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
    """
    génère un graphe orienté (non pondéré)
    """
    list_sommets = [i for i in range(nb_sommets)]
    list_arc = [(i,j) for i in range(nb_sommets) for j in range(nb_sommets) if np.random.random()<p and i!=j]
    list_poids = [1 for _ in range(len(list_arc))]

    return list_sommets, list_arc, list_poids

# plus vraiment besoin car Bellman-Ford peut faire la vérification en O(n)
def check_circuit_negatif(graphe):
    list_sommets,list_arc=graphe
    A=np.zeros((len(list_sommets),len(list_sommets)))

    for i in range(len(list_sommets)):
        for j in range(len(list_sommets)):
            if i!=j:
                A[(i,j)]=1000

    for arc in list_arc:
        A[list_sommets.index(arc[0])][list_sommets.index(arc[1])]=arc[2]

    for _ in range(len(list_sommets)):
        for k in range(len(A)):
            for i in range(len(A)):
                for j in range(len(A[i])):
                    A[(i,j)]=min(A[(i,j)],A[(i,k)]+A[(k,j)])
    
    for i in range(len(A)):
        if A[(i,i)]!=0:
            return True #Circuit detecté
        
    return False #NO CIRCUIT

def change_weight(G):
    """
    change le poids des arcs
    retourne les nouveaux poids
    """
    S, A, W = copy.deepcopy(G)
    newW = np.random.randint(-3, 11, size=len(W))

    return (S, A, newW)

def test(nbS, p, nbApp):
    """
    nbS (int) : nombre de sommets à générer
    p (float) : proba que l'arc (i, j) soit générer
    npApp (int) : nombre de graphes d'apprentissages, >= 3
    """
    if nbApp < 3:
        raise NameError("nbApp doit être plus grand que 3")
    
    G = genere_graphe(nbS, p)

    print("\nG =", G)
    dist, _, _ = bellman_Ford(G)
    dist = np.where(np.isinf(dist), dist, 1)
    _, counts = np.unique(dist, return_counts=True)

    # si le sommet source choisit n'atteint pas |V|/2 sommets, on change le sommets source
    while counts[0] < np.ceil(len(G[0])/2)+1:
        pop = G[0].pop(0)
        G[0].append(pop)
        dist, _, _ = bellman_Ford(G)
        dist = np.where(np.isinf(dist), dist, 1)
        _, counts = np.unique(dist, return_counts=True)

    # génération du graphe test H
    H = change_weight(G)
    res = bellman_Ford(H)
    while(res == False):
        H = change_weight(G)
        res = bellman_Ford(H)
    print("\nH =", H)

    list_nbIter = []
    for n in range(3, nbApp+1):
        # création des N graphes d'apprentissages et ses arboresences
        list_arboresence = []
        N = n
        cpt = 0
        while cpt < N:
            newG = change_weight(G)
            res = bellman_Ford(newG)
            if(res != False):
                _, arboresence, _ = res
                list_arboresence += arboresence
                cpt += 1
                #print("\nG%d ="%cpt, newG)

        # union des arboresences des plus courts chemins des graphes d'apprentissages
        T = list(set(list_arboresence))
        T.sort()
        #print("\nT =", T)

        # calcul de l'ordre <tot de T
        ordre = gloutonFas((G[0], T))
        dist, _, nbIter = bellman_Ford((ordre, H[1], H[2]))
        print("\npour %d graphes appris :\nordre <tot="%n, ordre)
        print("avec dist =", dist)
        list_nbIter.append(nbIter)

    # ordre aléatoire
    ordre_aleatoire = copy.copy(ordre)
    np.random.shuffle(ordre_aleatoire)
    # on conserve toujours le même sommet source
    ordre_aleatoire.remove(G[0][0])
    ordre_aleatoire = [G[0][0]] + ordre_aleatoire
    distA, _, nbIterA = bellman_Ford((ordre_aleatoire, H[1], H[2]))
    distA_p = np.where(np.isinf(distA), distA, 1)
    _, counts = np.unique(distA_p, return_counts=True)
    # si le sommet source n'atteint pas |V|/2 sommets, on change le source
    while counts[0] < np.ceil(len(G[0])/2)+1:
        np.random.shuffle(ordre_aleatoire)
        distA, _, nbIterA = bellman_Ford((ordre_aleatoire, H[1], H[2]))
        distA_p = np.where(np.isinf(distA), distA, 1)
        _, counts = np.unique(distA_p, return_counts=True)
    print("\nordre_aleatoire =", ordre_aleatoire)
    print("avec dist =", distA)
    
    # plot courbe nbIter en fonction de nbApp
    x = [i for i in range(3, nbApp+1)]
    plt.plot(x, list_nbIter, label="nbIter avec apprentissage", color='b')
    plt.plot(x, [nbIterA]*len(x), label="nbIter avec ordre aléatoire", color='r', linestyle='--')
    plt.legend()
    plt.show()
