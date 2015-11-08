# import networkx as nx

# k = raw_input("Enter genus: ")
k = 4


"""
class RotationSystem:

Initialize it with a dictionary of nodes:edgeCycle pairs

E.g., one RotationSystem for the eye graph would be:

rotSysList = {1:(1,2,3,4), 2:(2,3,1,4)}
myRotSys = RotationSystem(rotSysList)

Then you can do:

myRotSys.edges
myRotSys.nodes
myRotSys.nextUndirEdge(node,currentEdge)
myRotSys.nextDirEdge(node,currentEdge)
myRotSys.eulerChar

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

	def nextDirEdge(self, node, edge):
		nextUndirEdge = self.nextEdge(node, edge)
		#return the correct dir edge (has the right "to" node)
		if self.dirEdges[(nextUndirEdge,True)][0] is node:
			return (nextUndirEdge,True)
		else:
			return (nextUndirEdge, False)