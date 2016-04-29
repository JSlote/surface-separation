import networkx as nx

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
						
			
def filterIsomorphics(matrixList):
	reducedMatrixList = []
	for i in range(len(matrixList)):
		if matrixList[i] is 0:
			continue
		for j in range(i+1,len(matrixList)): #for each pair of graphs
			igraph = matrixToGraph(matrixList[i])
			jgraph = matrixToGraph(matrixList[j])
			if matrixList[j] is 0:
				continue
			if matrixList[i] not in reducedMatrixList:
				reducedMatrixList.append(matrixList[i])
			if nx.is_isomorphic(igraph,jgraph):
				matrixList[j] = 0
				
	graphlist = []