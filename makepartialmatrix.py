
def makePartialMatrix(list):
	partialmatrix = []
	for i in range(len(list)):
		partialmatrix.append([])
		for j in range(len(list)-i):
			partialmatrix[i].append(0)
	print partialmatrix

makePartialMatrix([10,10,10])