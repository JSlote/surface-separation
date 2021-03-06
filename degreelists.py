

def specialpartition(number):
	answer = set()
	answer.add((number, ))
	for x in range(4, number, 2):
		for y in specialpartition(number - x):
			answer.add(tuple(sorted((x, ) + y)))
	answer = list(answer)
	list2 = []
	for tuples in answer:
		if 2 not in tuples:
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
			else:
				pass
			numedge = numedge + 1
	listoftuplesfinal = []
	for tuple in listoftuples:
		l = list(tuple)
		listoftuplesfinal.append(l)

	return listoftuplesfinal

# print generateDegreeLists(2,1)