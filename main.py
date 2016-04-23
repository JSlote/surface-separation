For each legit degree list
	generate list of adjacency matrices
	remove isomorphic graphs in this smaller list (using NetworkX)
	add small list to big list!

For each adjacency matrix
	loop through rotation systems
		if we hit one that is both minimal and satisfies bounds
			add the adjacency matrix to our legit list
			break



from donutfuntimez import *


from graphgen import *
from graphfilter import *

for deglist in generateDegreeLists(n,k):
	tempList = generateAdjacencyMatrices(deglist)
	legitList = filterIsomorphics(tempList)
	bigList.append(legitList)

	
