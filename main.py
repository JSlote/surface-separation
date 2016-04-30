from graphgen import *
from graphfilter import *
import networkx as nx

k=2 #THIS MUST REMAIN AT 2 FOR NOW
g=1

matrixPossibilities = []

for deglist in generateDegreeLists(k,g): #k,g
	print deglist
	tempList = generateAdjacencyMatrices(deglist)
	print tempList
	legitList = filterIsomorphics(tempList)
	matrixPossibilities += legitList

minTwoCutGraphs = []

for adjacencyMatrix in matrixPossibilities:
	for rawRotationSystem in allRotationSystems(adjacencyMatrix):
		#initial rotation systems into objects with all the methods we need
		rotationSystem = RotationSystem(rawRotationSystem)
		if rotationSystem.isMinimal():
			c = rotationSystem.countDirectedCycles()
			v = len(rotationSystem.nodes)
			e = len(rotationSystem.undirEdges)
			if g >= 0.5*(c - v + e) - k + 1: #bound is satisfied
				minTwoCutGraphs.append(rawRotationSystem)
				# we don't need to check any other rotation systems for
				# this graph, so...
				break

print minTwoCutGraphs