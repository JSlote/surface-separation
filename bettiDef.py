import networkx as nx
from graphgen import *
from copy import *
import itertools
from filterIsomorphics import *


def graphToDict(g):
    '''
    Intakes a graph and outputs a dictionary of edges and how many times they appear

    Parameters:
    g (networkx multigraph object) - the original graph object

    Returns:
    graphDict (dictonary) - g as a dictionary. The edges are the keys and the number of times it
    appears is the value.
    '''
    gEdges = g.edges() #gets the list of edges in g

    graphDict = {} #creates the dictionary to hold the graph in

    for edge in gEdges:
        if edge in graphDict: 
            graphDict[edge] += 1 #if this edge has appeared before, add one to the value
        else:
            graphDict[edge] = 1 #if this edge hasn't appeared before, add the edge to the dictionary with value 1
    
    return graphDict #returns the dictionary of graph edges

def dictToGraph(gDict):
    '''
    Intakes the dictionary version of the graph and returns as a networkx multigraph object

    Parameters:
    gDict (dictionary) - the dictionary version of the graph

    Returns;
    g (networkx multigraph object) - the graph as a graph object
    '''

    gEdges = [] #creates the list we wil put the edges in
    edges = gDict.keys() #gets the list of edges we are working with

    for key in edges:
        for i in xrange(gDict[key]):
            gEdges.append(key)
    
    g = nx.MultiGraph()
    g.add_edges_from(gEdges)

    return g

def removeST(g, spanTree):
    '''
    Intakes a graph and a spanning tree and removes the spanning tree from the graph,
    creating a cotree

    Parameters:
    g (networkx multigraph object) - the original graph object
    spanTree (networkx multigraph object) - the spanning tree graph object

    Returns:
    cotree (networkx multigraph object) - the cotree graph object
    '''
    #gets the dictionary of the graph and edges of the spanning tree and graph and creates a dictionary object for the cotree
    gDict = graphToDict(g)
    gKeys = gDict.keys()
    stEdges = spanTree.edges()
    ctDict = {}

    for key in gKeys:
        if (key in stEdges) or (maxMin(key) in stEdges):
            ctDict[key] = gDict[key] - 1 #if the edge is in the spanning tree, subtract one
        else:
            ctDict[key] = gDict[key] #if the edge is not in the spanning tree, leave the value alone

    cotree = dictToGraph(ctDict)

    return cotree

def maxMin(edge):
    '''
    Sets an edge to be (max,min)

    Parameters:
    edge (tuple) - the original edge

    Returns:
    newEdge (tuple) - the edge with the larger number first
    '''

    ma = max(edge)
    mi = min(edge)

    newEdge = (ma, mi)

    return newEdge

def multipleCotrees(g):
    '''
    Given a grah, calculates all possible spanning trees, removes duplicates, and returns them

    Parameters:
    g (netwokrx multigraph object) - the original graph object

    Returns:
    cotrees (list of networkx multigraph objects) - all of the cotrees of g
    '''
    gEdges = g.edges()
    numEdges = len(gEdges)

    cotrees = []

    if len(g.nodes()) == 1:
        cotrees.append(graphToDict(g))
    else:
        trees = findAllSpanningTrees(g)
        for tree in trees:
            cotree = removeST(g, tree)
            cotrees.append(cotree)

    cotrees = filterIsos(cotrees)

    return cotrees


def subgraphs(g):
    '''
    Creates a list of all of the one-edge deleted subgraphs of a graph

    Parameters:
    g (networkx multigraph object) - the original grpah object

    Returns:
    subs (list of networkx multigraph objects) - all of the subgraphs of g where one edge of g has been removed
    '''
    edges = list(g.edges())
    subs = []
    
    for edge in edges:
        sub = deepcopy(edges)
        sub.remove(edge)
        subg = nx.MultiGraph()
        subg.add_edges_from(sub)
        subs.append(subg)

    
    subs = filterIsos(subs)

    return subs

def calcBetti(g):
    '''
    Calculates the first betti number of a graph

    Parameter:
    g (networkx multigraph object) - the original graph

    Returns:
    bettiNum (int) - the first betti number of a graph
    '''
    numEdges = len(g.edges())
    numVert = len(g.nodes())
    connComp = nx.number_connected_components(g)
    bettiNum = numEdges - numVert + connComp

    return bettiNum

def calcBettiDef(g):
    '''
    Calculates the betti deficiency of a graph

    Parameters:
    g (networkx multigraph object) - the original graph

    Returns:
    bDef (int) - the betti deficiency of the graph
    '''

    comps = [g.subgraph(c).copy() for c in nx.connected_components(g)]
    bDef = 0

    for curg in comps:
        cotrees = multipleCotrees(curg)
        minNum = len(curg.edges())
        for curCoTree in cotrees:
        
            if type(curCoTree) is dict:
                curCoTree = dictToGraph(curCoTree)
    
            currNum = 0

            components = [curCoTree.subgraph(c).copy() for c in nx.connected_components(curCoTree)]
            for part in components:
                if len(part.edges()) % 2 == 1:
                    currNum += 1
            if currNum < minNum:
                minNum = currNum
            
        bDef = bDef + minNum

    return bDef


def findAllSpanningTrees(g):
    '''
    Finds all spanning trees of a graph

    Parameters:
    g (networkx multigraph object) - the original graph
    
    Returns:
    trees (list of networkx multigraph objects) - list of spanning trees of g
    '''

    if not nx.is_connected(g):
        print "Warning: graph is not connected"

    numVert = len(g.nodes())
    edges = list(g.edges())

    trees = list(itertools.combinations(edges, numVert-1))
    
    treeList = []

    for tree in trees:
        graph = nx.MultiGraph()
        graph.add_edges_from(list(tree))
        poss = True
        if len(graph.nodes()) != numVert:
            poss = False
        if not nx.is_connected(graph):
            poss = False
        if poss:
            treeList.append(graph)
    

    return treeList

def min2cut(g, genus):
    '''
    Determines whether or not g can be a minimal two cut on a torus of the given genus using the subgraph test

    Parameters:
    g (networkx multigraph object) - the original graph
    genus (int) - the torus of the genus

    Retursn:
    possibility (boolean) - whether or not g can be a min 2 cut on specified genus
    '''
    subs = subgraphs(g)
    possibility = True

    for sub in subs:
        #print sub.edges()
        betti = calcBetti(sub)
        #print betti
        bettiDef = calcBettiDef(sub)
        #print bettiDef
        if genus < ((betti + bettiDef) / 2):
            possibility = False

    return possibility



def filterIsos(graphList):
    reducedGraphList = []
    for i in range(len(graphList)):
        if graphList[i] is 0:
		    continue
        for j in range(i+1,len(graphList)): #for each pair of graphs
			if graphList[j] is 0:
				continue
			if graphList[i] not in reducedGraphList:
				reducedGraphList.append(graphList[i])
			if nx.is_isomorphic(graphList[i],graphList[j]):
				graphList[j] = 0
    if graphList[-1] is not 0:
        reducedGraphList.append(graphList[-1])

    return reducedGraphList


def bettiFilter(origList, genus):
    twoCuts = []
    count = 1
    for matrix in origList:
        print "Checking graph ", count, " of ", len(origList)
        graph = matrixToGraph(matrix)
        poss = min2cut(graph,genus)
        if poss:
            twoCuts.append(matrix)
        count += 1
    return twoCuts






'''def main():
    G = nx.MultiGraph()
    edges = [(1,1),(1,2),(2,3),(1,3)]
    G.add_edges_from(edges)
    print G.edges()
    gDict = graphToDict(G)
    print gDict
    gObject = dictToGraph(gDict)
    print gObject.edges()
    print "-----------"
    matrix = [[0, 4], [0]]
    H = matrixToGraph(matrix)
    print H.edges()
    hDict = graphToDict(H)
    print graphToDict(H)
    hObj = dictToGraph(hDict)
    print hObj.edges()

    edge = (3,5)
    print maxMin(edge)
    print "-----------"

    print(subgraphs(G)[0].edges())
    print(subgraphs(G)[1].edges())
    print(subgraphs(G)[2].edges())

    print "-------------------"
    H = nx.MultiGraph()
    edges = [(1,1),(1,1),(2,2),(2,2)]
    H.add_edges_from(edges)
    
    S = [H.subgraph(c).copy() for c in nx.connected_components(H)]
    print(S[0].edges())
    print(S[1].edges())

    print "-----------------"

    print(multipleCotrees(G)[0].edges())
    print(multipleCotrees(G)[1].edges())

    print "----------------"
'''
'''
def main():
    G = matrixToGraph([[14]])
    print G.edges()
    #print calcBettiDef(G)
    #print calcBetti(G)
    print min2cut(G,3)

    print "----------"


main()
'''