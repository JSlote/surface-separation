from itertools import permutations as perms

def mergeDicts(x, y):
	'''Given two dicts, merge them into a new dict as a shallow copy.'''
	z = x.copy()
	z.update(y)
	return z

"""
class RotationSystem:

Initialize it with a dictionary of nodes:edgeCycle pairs
E.g., one RotationSystem for the eye graph would be:
rotSysList = {1:[1,2,3,4], 2:[2,3,1,4]}
myRotSys = RotationSystem(rotSysList)

Then you can do:

myRotSys.edges
myRotSys.nodes
myRotSys.nextUndirEdge(node,currentEdge)
myRotSys.nextDirEdge(node,currentEdge)
myRotSys.eulerChar
"""
class RotationSystem(object):
	# removes loops in G to make counting easier
	@staticmethod
	def __loopFree(G):
		loopFreeG = {}
		for node in G:
			loops = []
			edges = []
			for edge in G[node]:
				if G[node].count(edge) == 2:
					if edge not in loops:
						loops.append(edge)
						edges.append((edge,True))
					else:
						edges.append((edge,False))
				else:
					edges.append(edge)

			for edge in loops:
				# edges.extend([(edge,True),(edge,False)])
				loopFreeG[(node,edge)] = [(edge,True),(edge,False)]

			loopFreeG[node] = edges
		return loopFreeG
	
	def __init__(self, G):
		self.nodes = self.__loopFree(G)

		edges = {}
		for node in self.nodes:
			for edge in self.nodes[node]:
				if edge in edges:
					edges[edge][1] = node
				else:
					edges[edge] = [node, None]

		self.undirEdges = edges
		self.dirEdges = {}
		for edge in self.undirEdges:
			self.dirEdges[(edge,True)] = self.undirEdges[edge]
			#also add the other direction
			self.dirEdges[(edge,False)] = self.undirEdges[edge][::-1]

		self.eulerChar = len(self.nodes) - len(self.undirEdges)

	def nextUndirEdge(self, node, edge):
		theCycle = self.nodes[node]
		currentEdgeIndex = theCycle.index(edge)
		nextEdgeIndex = (currentEdgeIndex+1) % len(theCycle)
		return theCycle[nextEdgeIndex]

	def nextDirEdge(self, edge):
		inboundNode = self.dirEdges[edge][1]
		nextUndirEdge = self.nextUndirEdge(inboundNode, edge[0])
		#return the correct dir edge (has the right "to" node)
		if self.dirEdges[(nextUndirEdge,True)][0] is inboundNode:
			return (nextUndirEdge, True)
		else:
			return (nextUndirEdge, False)

	def countDirectedCycles(self):
		waitingEdges = self.dirEdges.keys()
		cycles = []
		while waitingEdges: #is not empty
			currentEdge = waitingEdges[0]
			thisCycle = []
			while currentEdge not in thisCycle:
				waitingEdges.remove(currentEdge)
				thisCycle.append(currentEdge)
				currentEdge = self.nextDirEdge(currentEdge)
			cycles.append(thisCycle)

		return len(cycles)

	#this only works for 2-cuts
	def isMinimal(self):
		waitingNodes = []

		# Pick an arbitrary edge in self
		firstEdge = next(self.undirEdges.iterkeys())

		# Assign it a direction arbitrarily

		# edgeDirDict holds assigned directions
		# key is edge, value is "to" node
		edgeDirDict = { firstEdge : self.undirEdges[firstEdge][1]}

		# Add the two nodes incident to that first edge to waitingNodes
		waitingNodes = list(self.undirEdges[firstEdge])

		while waitingNodes: # while waitingNodes has nodes in it
			# Pop vertex V from Waiting
			currNode = waitingNodes.pop()
			# Find an edge incident to currNode that has a direction already assigned:
			currNodeEdgeList = self.nodes[currNode]
			for i in xrange(len(currNodeEdgeList)):
				if currNodeEdgeList[i] in edgeDirDict:
					startEdgeIndex = i
					break

			# Try to assign directions alternating between inward and outward along the cyclic ordering.
			# create a variable to toggle 'away' and 'to'
			shouldBeToCurrNode = edgeDirDict[currNodeEdgeList[startEdgeIndex]] is not currNode
			# iterate through the other edges
			for i in xrange(len(currNodeEdgeList)-1):
				index = (startEdgeIndex + i + 1) % len(currNodeEdgeList)
				edge = currNodeEdgeList[index]
				if edge in edgeDirDict:
					# if the current edge in question already had an incompatible direction assigned
					if (edgeDirDict[edge] == currNode) is not shouldBeToCurrNode:
						return False
					#else, it's already correct
				else: #the current edge doesn't have a direction assigned yet
					otherNodeOfEdge = self.undirEdges[edge][1] if (self.undirEdges[edge][0] == currNode) else self.undirEdges[edge][0]
					# Add vertices incident to each edge that is newly assigned a direction to Waiting
					waitingNodes.append(otherNodeOfEdge)
					edgeDirDict[edge] = currNode if shouldBeToCurrNode else otherNodeOfEdge

				shouldBeToCurrNode = not shouldBeToCurrNode

		return True #(we had no problems)

def allRotationSystems(adjacencyMatrix):
	#convert adjacency matrix to rotation-system-like format
	numNodes = len(adjacencyMatrix[0])
	G = {k: [] for k in range(1,numNodes+1)}
	currEdgeIndex = 0
	for row in xrange(numNodes):
		for column in xrange(row,numNodes): #column index as if we're looping through the upper diagonal
			numHalfEdgesToPlace = adjacencyMatrix[row][column-row]
			if row is column: #because the following loop places have edges in the "leaving" node and the "arriving" node, it doubles our half edges for loops.
				numHalfEdgesToPlace /= 2
			for edgeIndexOffset in range(1,numHalfEdgesToPlace+1):
				G[row+1].append(currEdgeIndex+edgeIndexOffset)
				G[column+1].append(currEdgeIndex+edgeIndexOffset)
			currEdgeIndex += adjacencyMatrix[row][column-row]

	def recurse(remainingNodes):
		edges = G[remainingNodes[0]]
		# because these are cyclic permutations, we fix the first element
		for partialPerm in perms(edges[1:]):
			if len(remainingNodes) == 1:
				yield {remainingNodes[0] : edges[:1]+list(partialPerm)}
			else:
				# print {remainingNodes[0] : edges[:1]+list(partialPerm)}
				# print recurse(remainingNodes[1:]
				for followingPerms in recurse(remainingNodes[1:]):
					yield mergeDicts({remainingNodes[0] : edges[:1]+list(partialPerm)}, followingPerms)

	return recurse(G.keys())