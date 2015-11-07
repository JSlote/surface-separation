# import networkx as nx

# k = raw_input("Enter genus: ")
k = 4


"""
class RotationSystem:

Initialize it with a dictionary of nodes and a dictionary of edges:

E.g., the eye:

nodes = {1:(1,2,3,4), 2:(2,3,1,4)}
edges = {1:(1,2),2:(1,2),3:(1,2),4(1,2)}

myRotSys = RotationSystem(nodes, edges)

TODO: There is a little redundancy in this init. Let's try to fix that.
"""
class RotationSystem(object):
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.undirEdges = edges
		self.dirEdges = {}
		for edge in self.undirEdges:
			self.dirEdges[(edge,True)] = self.undirEdges[edge]
			#also add the other direction
			self.dirEdges[(edge,False)] = self.undirEdges[edge][::-1]

	def nextEdge(self, node, edge):
		cycle = self.nodes[node]
		currentEdgeIndex = cycle.index(edge)
		nextEdgeIndex = cycle[(currentEdgeIndex+1) % len(cycle)]
		return cycle[nextEdgeIndex]

	def nextDirEdge(self, node, edge):
		nextUndirEdge = self.nextEdge(node, edge)
		if self.dirEdges[(nextUndirEdge,True)][0] is node:
			return (nextUndirEdge,True)
		else:
			return (nextUndirEdge, False)