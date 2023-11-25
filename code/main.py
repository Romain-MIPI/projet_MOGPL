from methode import * 

# graphes n'ayant pas de cycle absorbant
g_projet=[[1,2,3,4,5,6,7,8],[(1,2,1),(1,3,1),(2,3,1),(3,4,1),(4,5,1),(4,6,1),(4,7,1),(5,7,1),(6,5,1),(6,8,1),(7,1,1),(8,3,1),(8,2,1)]]
#g_projet = [["A", "B", "C", "D", "E"], [("A", "B", -1), ("A", "C", 4), ("B", "C", 3), ("B", "D", 2), ("B", "E", 2), ("D", "B", 1), ("D", "C", 3), ("E", "D", -3)]]

# graphes ayant un cycle absorbant
#g_projet=[[1,2,3,4,5,6,7,8],[(1,2,1),(1,3,1),(2,3,1),(3,4,1),(4,5,1),(4,6,1),(4,7,1),(5,7,1),(6,5,1),(6,8,1),(7,1,-4),(8,3,1),(8,2,1)]]
#g_projet = [["A", "B", "C", "D", "E"], [("A", "B", -1), ("A", "C", 4), ("B", "C", 3), ("B", "D", 2), ("B", "E", 2), ("D", "B", 1), ("D", "C", 3), ("E", "D", -4)]]

arr = gloutonFas(g_projet)

#print(arr)
#print(bellman_Ford(g_projet))
#print(bellman_Ford((arr, g_projet[1])))


test()