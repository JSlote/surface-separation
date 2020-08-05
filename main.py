# Here's where things stand:
# 2. We need to take another look at the degree list generation
# because I had to modify it but I don't trust my modifications

# --Joe


from graphgen import *
from graphfilter import *
import networkx as nx
import sys
from bettiDef import *

k = 2 #THIS MUST REMAIN AT 2 FOR NOW
g = 3

matrixPossibilities = []

numGraphs = 0
count = 0
total = len(generateDegreeLists(k,g))
for deglist in generateDegreeLists(k,g): #k,g
	count += 1
	print "Start"
	tempList = generateAdjacencyMatrices(deglist)
	print "matrices generated", len(tempList)
	legitList = filterIsomorphics(tempList)
	print "isos filtered"
	filteredList = bettiFilter(legitList, g)
	matrixPossibilities += filteredList
	numGraphs += len(filteredList)
	sys.stdout.write("\r Working on degree list " + str(count) + " out of " + str(total)+ ". Number of possible graphs: "+ str(numGraphs) )
	sys.stdout.flush()

possibleGraphsFile = open("possiblegraphs.txt", "w")
for graph in matrixPossibilities:
	possibleGraphsFile.write(str(graph)+"\n")
possibleGraphsFile.close()

minTwoCutGraphs = []

numPossibilities = len(matrixPossibilities)
print "\nFinished constructing superset of", numPossibilities, "possible graphs."
'''

minTwoCutGraphs = []
numPossibilities = 6
matrixPossibilities = []

graphs = open("possiblegraphs.txt", "r")
for line in graphs:
	matrix = line.rstrip()
	matrix = list(matrix)
	matrixPossibilities.append(matrix)

graphs.close()
'''
for i in xrange(numPossibilities):
	adjacencyMatrix = matrixPossibilities[i]
	percentDone = (100*i) / numPossibilities
	sys.stdout.write("\rCurrent Status: %d%% complete; analyzing %s" % (percentDone, adjacencyMatrix))
	sys.stdout.flush()
	count = 0
	for rawRotationSystem in allRotationSystems(adjacencyMatrix):
		print(percentDone, " ", adjacencyMatrix, " ", count)
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
		count += 1

print "\nGraph filtering complete. Here are min-"+str(k)+"-cuts on a",str(g)+"-torus:"
for graph in minTwoCutGraphs:
	print graph[0]
	# print nx.convert_matrix[graph[1]]