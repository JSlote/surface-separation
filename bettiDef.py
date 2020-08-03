import networkx as nx
from graphgen import *

# function to determine if the graph, G, passes the subgraph test
    # in: graph in edgelist format (or graph format)
    # out: boolean that is whether the graph is still a possibility

    # makes a list of subgraphs of G
    # sets variable "possibility" to true
    # for each subgraph:
        #calculate the betti number
        # calculate the betti deficiency
        # If betti + def /2 > genus of surface:
            # possibility = false
            # break
    # return possibility

# function to make a list of the subgraphs of G
    # in: graph is edgelist format (or graph format)
    # out: list of subtrees in edge list format

    # create list of edges in G
    # make an empty list to hold the subtrees

    # for each edge in the edgelist drop the edge and add it to the list of subtrees

    # delete exact duplicates

    # make a list of graphs from the edge lists

    # delete isomorphisms and make a new list
    # clear list of subtrees

    # recreate edge list based on list of graphs


# function to calculate the betti number of G
    # in: g, original graph in edgelist format
    # out: betti number

    # calculate numedges -> length of edge list
    # caluclate number of vertices -> length of vertex list
    # caluclate connected components -> length of connected components
    # betti = edges - vert + connComp
    # return betti

# function to calculate the betti def of G
    #in: g, in edgelist format
    # out: betti def of graph

    # calculate all of the cotrees of the graph
    # set minnum as length of edgelist of g

    # for each cotree, calcs the betti def and then takes the smallest one
        #currnum = 0
        # components = connected graph components of the graph of the cotree
        # for each component,
            # if the length of the edgelist of the component is odd, add 1 to currnum

        # if currnum < minNum, minnum = currNum


# function to calculate all of the cotrees of the graph
    #in: g, original graph in edge list format
    # out: list of cotree in list of edges format

    #calc numEdges

    # for each edge in G,
        # create weights table
        # change weight of this edge to 1
        # find the spanning tree using weights
        # get the cotree association with this spanning tree
        # append to the list of cotrees

# function that gets the cotree association given a graph and spanning tree

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

    cotrees (list of networkx multigraph objects) - all of the cotrees of g
    '''
    gEdges = g.edges()
    numEdges = len(gEdges)

    cotrees = []

    for m in xrange(numEdges):
        weights = [0]*numEdges
        weights[m] = 1
        spannTree = nx.minimum_spanning_tree(g, weight = weights)
        cotree = removeST(g,spannTree)
        cotrees.append(cotree)

    cotrees = filterIsos(cotrees)

    return cotrees




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
			if nx.is_isomorphic(i,j):
				graphList[j] = 0
				
    return reducedGraphList









def main():
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

    multipleCotrees(H)

main()
