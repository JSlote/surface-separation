
from copy import deepcopy



def matrixgen(currBuckets,partialMatrix,partialColIndex,rowIndex):

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

                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, 0, rowIndex+1)

                return solutionList

        elif rowIndex == partialColIndex+rowIndex: #we're at a diagonal

            # we can only write even numbers in here, so iterate through half the values and double

            for k in xrange(min(rowDegrees,columnDegrees)//2+1):

                updatedPartialMatrix = deepcopy(partialMatrix)

                updatedPartialMatrix[rowIndex][partialColIndex] = 2*k

                updatedBuckets = list(currBuckets)

                updatedBuckets[rowIndex] = rowDegrees-2*k

                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)

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

                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)

            return solutionList


from copy import deepcopy

def makePartialMatrix(list):
	partialmatrix = []
	for i in range(len(list)):
		partialmatrix.append([])
		for j in range(len(list)-i):
			partialmatrix[i].append(0)

def generateAdjacencyMatrices(currBuckets,partialMatrix,partialColIndex,rowIndex):
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
                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, 0, rowIndex+1)
                return solutionList
        elif rowIndex == partialColIndex+rowIndex: #we're at a diagonal
            # we can only write even numbers in here, so iterate through half the values and double
            for k in xrange(min(rowDegrees,columnDegrees)//2+1):
                updatedPartialMatrix = deepcopy(partialMatrix)
                updatedPartialMatrix[rowIndex][partialColIndex] = 2*k
                updatedBuckets = list(currBuckets)
                updatedBuckets[rowIndex] = rowDegrees-2*k
                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)
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
                solutionList = solutionList + matrixgen(updatedBuckets, updatedPartialMatrix, partialColIndex+1, rowIndex)
            return solutionList
               