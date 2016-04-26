# import networkx as nx
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

def allRotationSystems(G):
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

def main(k):

	legitList = []

	# import pdb; pdb.set_trace()
	graphs = [{1:[1,2,3,4], 2:[1,2,3,4]},
			  {1:[1,1,2,2,3,3]},
			  {1:[1,1]},
			  {1:[1,1,2,2]},
			  {1:[1,1,2,2,3,3,4,4]}]

	for G in graphs:
		for rotSys in allRotationSystems(G):
			TG = RotationSystem(rotSys)
			if not TG.isMinimal(): continue
			n = TG.countDirectedCycles()
			g = 1 - 0.5*TG.eulerChar - 0.5*n
			if g + n - 2 <= k:
				legitList.append(G)
				break
			#else: 'fails genus test'

	for legitGraph in legitList:
		print legitGraph

main(1)