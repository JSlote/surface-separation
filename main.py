# Here's where things stand:
# 2. We need to take another look at the degree list generation
# because I had to modify it but I don't trust my modifications

# --Joe


from graphgen import *
from graphfilter import *
import networkx as nx
import sys

k = 2 #THIS MUST REMAIN AT 2 FOR NOW
g = 1

matrixPossibilities = []

numGraphs = 0
for deglist in generateDegreeLists(k,g): #k,g
	tempList = generateAdjacencyMatrices(deglist)
	legitList = filterIsomorphics(tempList)
	matrixPossibilities += legitList
	numGraphs += len(legitList)
	sys.stdout.write("\rNumber of possible graphs: "+ str(numGraphs) )
	sys.stdout.flush()

possibleGraphsFile = open("possiblegraphs.txt", "w")
for graph in matrixPossibilities:
	possibleGraphsFile.write(str(graph)+"\n")
possibleGraphsFile.close()

minTwoCutGraphs = []

numPossibilities = len(matrixPossibilities)
print "\nFinished constructing superset of", numPossibilities, "possible graphs."

for i in xrange(numPossibilities):
	adjacencyMatrix = matrixPossibilities[i]
	percentDone = (100*i) / numPossibilities
	sys.stdout.write("\rCurrent Status: %d%% complete; analyzing %s" % (percentDone, adjacencyMatrix))
	sys.stdout.flush()
	for rawRotationSystem in allRotationSystems(adjacencyMatrix):
		#initial rotation systems into objects with all the methods we need
		rotationSystem = RotationSystem(rawRotationSystem)
		if rotationSystem.isMinimal(k):
			c = rotationSystem.countDirectedCycles()
			v = len(rotationSystem.nodes)
			e = len(rotationSystem.undirEdges)
			if g >= 0.5*(c - v + e) - k + 1: #bound is satisfied
				minTwoCutGraphs.append((rawRotationSystem,adjacencyMatrix))
				# we don't need to check any other rotation systems for
				# this graph, so...
				break

print "\nGraph filtering complete. Here are min-"+str(k)+"-cuts on a",str(g)+"-torus:"
for graph in minTwoCutGraphs:
	print graph[0]