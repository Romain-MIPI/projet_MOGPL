from methode import * 

# exemple du sujet
#G = [[1,2,3,4,5,6,7,8],[(1,2),(1,3),(2,3),(3,4),(4,5),(4,6),(4,7),(5,7),(6,5),(6,8),(7,1),(8,3),(8,2)], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# exemple du cours 6
#G = [["A", "B", "C", "D", "E"], [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("B", "E"), ("D", "B"), ("D", "C"), ("E", "D")], [-1, 4, 3, 2, 2, 1, 3, -3]]

# fonction de test
# test(n, p, nbApp)
# avec :
#     - n : nombre de sommets
#     - p : probabilité que l'arc (u, v) soit généré
#     - nbApp : nombre de graphe d'apprentissage maximum, nbApp > 3
test(10,0.3,100)