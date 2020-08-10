#  This will find rotation systems for possible min 2-cuts given as adjacency matrices in the file 'matrices.txt'

import ast
from graphgen import *
from graphfilter import *
import networkx as nx
import sys
from bettiDef import *

k = 2 #THIS MUST REMAIN AT 2 FOR NOW
g = 3

# Open and read in the file lines as a list of strings, eliminate \n's.
with open('mmaOutput.txt') as f:
    matrix_list_str = f.read().splitlines()
f.close()


# Convert each element of the string list into a list of ints.
matrixPossibilities = map(ast.literal_eval,matrix_list_str)

minTwoCutGraphs = []
numPossibilities = len(matrixPossibilities)

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