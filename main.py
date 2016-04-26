# For each legit degree list
# 	generate list of adjacency matrices
# 	remove isomorphic graphs in this smaller list (using NetworkX)
# 	add small list to big list!

# For each adjacency matrix
# 	loop through rotation systems
# 		if we hit one that is both minimal and satisfies bounds
# 			add the adjacency matrix to our legit list
# 			break

k=2
g=1


# from graphgen import *
from graphfilter import *
import networkx as nx

# for deglist in generateDegreeLists(n,k):
# 	tempList = generateAdjacencyMatrices(deglist)
# 	legitList = filterIsomorphics(tempList)
# 	bigList.append(legitList)

minTwoCutGraphs = []

matrixPossibilities = [[[0,4],[0]]]

for adjacencyMatrix in matrixPossibilities:
	for rawRotationSystem in allRotationSystems(adjacencyMatrix):
		rotationSystem = RotationSystem(rawRotationSystem)
		if rotationSystem.isMinimal():
			c = rotationSystem.countDirectedCycles()
			v = len(rotationSystem.nodes)
			e = len(rotationSystem.undirEdges)
			if g >= 0.5*(c - v + e) - k + 1: #bound is satisfied
				minTwoCutGraphs.append(rawRotationSystem)
				break

print minTwoCutGraphs