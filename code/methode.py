import numpy as np
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
    dist = [np.inf] * len(sommets) #matrice de distance, stoque que dist[k] et dist[k+1] à chaque itération
    pred = [None] * len(sommets)    #liste de sommet prédecesseur
    dist[sommets.index(src)] = 0
    conv = False
    
    for i in range(0, len(sommets)):
        conv = True
        for u in sommets:
            # arc = (v, u)
            for j, arc in enumerate(arcs):
                if arc[1] == u:
                    v = arc[0]
                    w = poids[j]
                    indu, indv = sommets.index(u), sommets.index(v)
                    if dist[indv]+w < dist[indu]:
                        dist[indu] = dist[indv]+w
                        pred[indu] = v
                        conv = False
        
        #print("dist =", dist)
        #print("pred =", pred)

        if conv:  #si convergence
            return dist, construction_arboresecnce(graphe, src, pred), i

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

def change_weight(G):
    """
    change le poids des arcs
    retourne les nouveaux poids
    """
    S, A, W = copy.deepcopy(G)
    newW = np.random.randint(-3, 11, size=len(W))

    return (S, A, newW)

#Questions 6,7,8,9
def test(nbS, p, nbApp):
    """
    nbS (int) : nombre de sommets à générer
    p (float) : proba que l'arc (i, j) soit générer
    npApp (int) : nombre de graphes d'application, >= 3
    on fixe le nombre d'appretissage à 3
    """
    # génération de G et choix de sommet source
    G = genere_graphe(nbS, p)

    print("\nG =", G[:-1])
    dist, _, _ = bellman_Ford(G)
    dist = np.where(np.isinf(dist), dist, 1)
    _, counts = np.unique(dist, return_counts=True)
    cpt = 0 # compteur qui vérifie si on a vérifié pour tous les sommets

    # si le sommet source choisit n'atteint pas |V|/2 sommets, on change le sommets source
    while counts[0]-1 < np.ceil(len(G[0])/2):
        # aucun sommet source peut atteindre au moins |V|/2 sommets
        # on change de graphe
        if cpt == nbS:
            G = genere_graphe(nbS, p)
            cpt = 0
            dist, _, _ = bellman_Ford(G)
            dist = np.where(np.isinf(dist), dist, 1)
            _, counts = np.unique(dist, return_counts=True)
        
        # changement de sommet source et calcul de la nouvelle distance
        else:
            pop = G[0].pop(0)
            G[0].append(pop)
            cpt += 1
            dist, _, _ = bellman_Ford(G)
            dist = np.where(np.isinf(dist), dist, 1)
            _, counts = np.unique(dist, return_counts=True)

    H = change_weight(G)
    res = bellman_Ford(H)
    # res = dist, arborescence, nbIter si non circuit absorbant
    # res = False sinon
    while(res == False):
        H = change_weight(G)
        res = bellman_Ford(H)

    print("\nw_H =", H[2])

    list_nb_iter_app=[]
    list_arboresence=[]

    # calcul de l'ordre <tot
    # on fait 3 apprentissages par défaut
    for n in range(0, 3):
        newG=change_weight(G)
        res = bellman_Ford(newG)
        # res = dist, arborescence, nbIter si non circuit absorbant
        # res = False sinon
        while(res == False):
            newG = change_weight(G)
            res = bellman_Ford(newG)
        print("\nw%d ="%(n+1), newG[2])

        list_arboresence += res[1]

    # T : union des arborescences des plus courts chemin
    T = list(set(list_arboresence))
    T.sort()
    # calcul de l'ordre <tot de T
    ordre = gloutonFas((G[0], T))
    _, _, nbIter = bellman_Ford((ordre, H[1], H[2]))
    print("\npour 3 graphes appris :\nordre <tot=", ordre)
    print("nbIter =", nbIter)
    list_nb_iter_app.append(nbIter)

    # si nbApp > 3
    for n in range(3, nbApp):
        newG=change_weight(G)
        res = bellman_Ford(newG)
        # res = dist, arborescence, nbIter si non circuit absorbant
        # res = False sinon
        while(res == False):
            newG = change_weight(G)
            res = bellman_Ford(newG)
        print("\nw%d ="%(n+1), newG[2])

        list_arboresence += res[1]

        T = list(set(list_arboresence))
        T.sort()
        # calcul de l'ordre <tot de T
        ordre = gloutonFas((G[0], T))
        _, _, nbIter = bellman_Ford((ordre, H[1], H[2]))
        print("\npour %d graphes appris :\nordre <tot="%(n+1), ordre)
        print("nbIter =", nbIter)
        list_nb_iter_app.append(nbIter)

    # ordre aléatoire
    ordre_aleatoire = copy.copy(ordre)
    np.random.shuffle(ordre_aleatoire)
    # on conserve toujours le même sommet source
    ordre_aleatoire.remove(G[0][0])
    ordre_aleatoire = [G[0][0]] + ordre_aleatoire
    _, _, nbIterA = bellman_Ford((ordre_aleatoire, H[1], H[2]))
    print("\nordre_aleatoire =", ordre_aleatoire)
    print("nbIter =", nbIterA)

    if nbApp > 3:        
        x = [i for i in range(3, nbApp+1)]
        plt.xlabel("Nombre de graphe appris")
        plt.ylabel("Nombre d'itération nécessaire")
        plt.title("Nombre d'itération en fonction du nombre d'apprentissage")
        plt.plot(x, list_nb_iter_app, label="nbIter avec apprentissage", color='b')
        plt.plot(x, [nbIterA]*len(x), label="nbIter avec ordre aléatoire", color='r', linestyle='--')
        plt.legend()
        plt.savefig('res/courbe_nbIter_pour_%d_apprentissasges.png'%nbApp)
        plt.show()