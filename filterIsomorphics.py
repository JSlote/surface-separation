from networkx import *

def matrixToGraph(matrix):
	G=nx.MultiGraph()
	numNodes = len(matrix[0])
	G.add_nodes_from(range(1,numNodes+1))
	for row in xrange(numNodes):
		for column in xrange(row, numNodes):
			numHalfEdgestoPlace = matrix[row][column-row]
			if row is column:
				numHalfEdgestoPlace /= 2
			for i in range(numHalfEdgestoPlace):
				G.add_edge(row,column)
	return [G]
						
			
def filterIsomorphics(listofmatrices):
	graphswextra = []
	for list in listofmatrices:
		graphswextra.append(matrixToGraph(list))
	graphlist = []
	for i in len(graphswextra): 
		for j in range(i+1,len(graphswextra)): #for each pair of graphs
			if is_isomorphic(graphswextra[i],graphswextra[j]) == False:
				if graphswextra[i] notin graphlist:
					graphlist.append(graphswextra[i],graphswextra[j]) #if not isomorphic and first list isn't already in list, 
					#append both to master list
				else: #if first list is already there, append second to list
					graphlist.append(graphswextra[j])
			else: #if isomorphic
				graphswithextra[j] = 0
				if graphswithextra[i] notin graphlist:
					graphlist.append(graphswextra[i]) #if first list isn't already in list, append it (if it's already there, do nothing)
	legitgraphlist = []
	for list in graphlist:
		if list != 0:
			legitgraphlist.append(list)
