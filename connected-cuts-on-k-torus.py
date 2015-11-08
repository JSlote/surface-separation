# import networkx as nx

# k = raw_input("Enter genus: ")
k = 4


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

TODO: currently can't handle loops:
The bouquet, {1:(1,3,2,1,3,2)}, won't work (I don't think)
"""
class RotationSystem(object):
	def __init__(self, rotSysList):
		self.nodes = rotSysList

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


def countDirectedCycles(TG):
	waitingEdges = TG.dirEdges.keys()
	cycles = []
	while waitingEdges: #is not empty
		currentEdge = waitingEdges[0]
		thisCycle = []
		while currentEdge not in thisCycle:
			waitingEdges.remove(currentEdge)
			thisCycle.append(currentEdge)
			currentEdge = TG.nextDirEdge(currentEdge)
		cycles.append(thisCycle)
	return len(cycles)

def isMinimal(TG):
	waitingNodes = []

	# Pick an arbitrary edge in TG
	firstEdge = next(TG.undirEdges.iterkeys())

	# Assign it a direction arbitrarily

	# edgeDirDict holds assigned directions
	# key is edge, value is "to" node
	edgeDirDict = { firstEdge : TG.undirEdges[firstEdge][1]}

	# Add the two nodes incident to that first edge to waitingNodes
	waitingNodes = list(TG.undirEdges[firstEdge])

	while waitingNodes: # while waitingNodes has nodes in it
		# Pop vertex V from Waiting
		currNode = waitingNodes.pop()
		# Find an edge incident to currNode that has a direction already assigned:
		currNodeEdgeList = TG.nodes[currNode]
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
				otherNodeOfEdge = TG.undirEdges[edge][1] if (TG.undirEdges[edge][0] == currNode) else TG.undirEdges[edge][0]
				# Add vertices incident to each edge that is newly assigned a direction to Waiting
				waitingNodes.append(otherNodeOfEdge)
				edgeDirDict[edge] = currNode if shouldBeToCurrNode else otherNodeOfEdge

			shouldBeToCurrNode = not shouldBeToCurrNode

	return True #(we had no problems)

rotSysList = {1:[1,2,3,4], 2:[1,4,3,2]}
myRotSys = RotationSystem(rotSysList)
print countDirectedCycles(myRotSys)
print isMinimal(myRotSys)
# import pdb; pdb.set_trace()