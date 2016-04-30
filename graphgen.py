# CURRENTLY WORKING ON:
# Tryna put the n lone loops on the first n rows of the adjacency matrix
# but they get re-written by the recursion
# instead, should leave recursion alone and suck up putting the 2s at
# the end of the matrix, adding as many 0s as necessary to the extant one


import networkx as nx
from copy import deepcopy

def specialpartition(number):
    answer = set()
    answer.add((number, ))
    for x in range(2, number, 2):
        for y in specialpartition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    answer = list(answer)
    list2 = []
    for tuples in answer:
        list2.append(tuples)
    return list2
    
def generateDegreeLists(k,g): #this does not yet depend on k (only works for k = 2)

    listoftuples = []
    for possv in range(1, 2*g+1): #range of possible vertices
        numedge = 2*possv #minimum possible number of edges
        while numedge <= 4*g: #4g is max possible number of edges 
            if numedge - possv <= 2*g: #another graph condition
                tuplist = specialpartition(numedge*2) #each edge contributes 2 to the 
                #degree list, hence the multiplying by 2; the special partition function
                #gives all possible degree lists such that each degree is even and \ge 4. 
                for tup in tuplist:
                    if len(tup) == possv: #want the partitions to have appropriate number of vertices, duh
                        listoftuples.append(tup)
            numedge = numedge + 1
    listoftuplesfinal = []
    for tuple in listoftuples:
        l = list(tuple)
        listoftuplesfinal.append(l)

    return listoftuplesfinal

def generateAdjacencyMatrices(deglist):
    def makeInitialMatrix(deglist, numberOfLoneLoops):
        partialmatrix = []
        for i in range(len(deglist)+numberOfLoneLoops):
            partialmatrix.append([])
            for j in range(len(deglist)+numberOfLoneLoops-i):
                if j == i and i < numberOfLoneLoops:
                    partialmatrix[i].append(2)
                else:
                    partialmatrix[i].append(0)
        print "partialmatrix", partialmatrix
        return partialmatrix

    def recurse(currBuckets, partialMatrix, partialColIndex, rowIndex):
        # partialMatrix is list of lists
        # index1 is index inside row
        # index2 is row
        # location in matrix [index2, index2+index1]

        #currbuckets is degreelist
        rowDegrees = currBuckets[rowIndex]
        columnDegrees = currBuckets[partialColIndex+rowIndex]

        # goes down the rows
        # while rowIndex <= len(currBuckets)-1: #cuz it starts at zero
                
        # BASE CASE:
        if partialColIndex == 0 and rowIndex == len(currBuckets)-1:
            partialMatrix[rowIndex][partialColIndex] = rowDegrees
            return [partialMatrix]
        
        # RECURSION STEP:
        # If we're not working on the very last cell:
        else:
            solutionList = []
            # if we're at the end of a row
            if partialColIndex == len(currBuckets)-1-rowIndex and rowIndex < len(currBuckets)-1:
            #   if we're screwed
                if rowDegrees > columnDegrees:
                    return []
            #   if we're not screwed, dump all of the row vertex's leftover degrees
                else:
                    updatedPartialMatrix = deepcopy(partialMatrix)  
                    updatedPartialMatrix[rowIndex][partialColIndex] = rowDegrees #dump rest in
                    updatedBuckets = list(currBuckets)
                    updatedBuckets[rowIndex] = 0
                    updatedBuckets[rowIndex + partialColIndex] = columnDegrees - rowDegrees
                    # make newBuckets and newPartialMatrix
                    solutionList = solutionList + recurse(updatedBuckets, updatedPartialMatrix, 0, rowIndex+1)
                    return solutionList
            elif rowIndex == partialColIndex+rowIndex: #we're at a diagonal
                # we can only write even numbers in here, so iterate through half the values and double
                for k in xrange(min(rowDegrees,columnDegrees)//2+1):
                    updatedPartialMatrix = deepcopy(partialMatrix)
                    updatedPartialMatrix[rowIndex][partialColIndex] = 2*k
                    updatedBuckets = list(currBuckets)
                    updatedBuckets[rowIndex] = rowDegrees-2*k
                    solutionList = solutionList + recurse(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)
                return solutionList
                
            # otherwise (we're not at the end of a row or on the diagonal)
            else:
            #     for all possible things less than that min(stuff)
                for k in xrange(min(rowDegrees,columnDegrees)+1):
                    updatedPartialMatrix = deepcopy(partialMatrix)
                    updatedPartialMatrix[rowIndex][partialColIndex] = k
                    updatedBuckets = list(currBuckets)
                    updatedBuckets[rowIndex] = rowDegrees-k
                    updatedBuckets[rowIndex + partialColIndex] = columnDegrees - k
                    solutionList = solutionList + recurse(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)
                return solutionList

    #Here we deal with vertices with valence 2 separately.
    #All verts of valence 2 MUST be their own loops (indeed,
    # below is the only check of this fact)
    # so count all such vs
    numberOfLoneLoops = deglist.count(2)
    print 'numberOfLoneLoops', numberOfLoneLoops
    # remove them from the matrix generation process
    deglist = [y for y in deglist if y != 2]

    return recurse(deglist,makeInitialMatrix(deglist, numberOfLoneLoops),numberOfLoneLoops,0)

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
    return G
                        
            
def filterIsomorphics(matrixList):
    reducedMatrixList = []
    for i in range(len(matrixList)):
        if matrixList[i] is 0:
            continue
        igraph = matrixToGraph(matrixList[i])
        if matrixList[i] not in reducedMatrixList:
            reducedMatrixList.append(matrixList[i])
        for j in range(i+1,len(matrixList)): #for each pair of graphs
            if matrixList[j] is 0:
                continue
            jgraph = matrixToGraph(matrixList[j])
            if nx.is_isomorphic(igraph,jgraph):
                matrixList[j] = 0
                
    return reducedMatrixList