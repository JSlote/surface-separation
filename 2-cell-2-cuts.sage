print """
This program will run indefinitely, counting the number of graphs
that can be embedded on the n-holed torus such that the surface is
paritioned into two cellular (homeomorphic to the disc) faces,
neither of which border themselves.

It will also save each set of graphs as a compressed Sage object
in the current directory.

Finally, it is has been optimized to run in parallel on your """ + str(sage.parallel.ncpus.ncpus()) + " cores.\n"

import sys

@parallel
def build_children(seedGraph):
    def pick_v(g):
        #given a g, returns all possible (graph, picked v) in a  list
        newGraphs = []
        for edge in g.edges():
            h = g.copy()
            startv = edge[0]
            endv = edge[1]
            h.delete_edge(edge)
            pickedV = h.add_vertex()
            h.add_edge(startv, pickedV)
            h.add_edge(pickedV, endv)
            yield (h, pickedV)
        for pickedV in g.vertices():
            h = g.copy()
            yield (h, pickedV)

    mutableG = seedGraph.copy(immutable = False)
    childSet = set()
    
    for tempGraph, firstV in pick_v(mutableG):
        for finalGraph, secondV in pick_v(tempGraph):
            finalGraph.add_edges([(firstV,secondV),(firstV,secondV)])
            setMember = finalGraph.canonical_label().copy(immutable=True)
            childSet.add(setMember)
    
    return childSet

def next_genus(seeds, verbose = False):
    #if verbose is True this function will
    #keep us updated on how many graphs have been found
    
    completeSet = set()
    completeSetLength = 0
    
    if verbose:
        for output in build_children(seeds):
            completeSet.update(output[1])
            sys.stdout.write("\r{} graphs...".format(len(completeSet)))
            sys.stdout.flush()
    else:
        for output in build_children(seeds):
            completeSet.update(output[1])

    if verbose:
        sys.stdout.write("\r{} graphs - done!".format(len(completeSet)))
        
    return list(completeSet)

g = Graph({0:[0,0,0]})
g.allow_loops(True)
g.allow_multiple_edges(True)

h = Graph({0:[],1:[0,0,0,0]})
h.allow_loops(True)
h.allow_multiple_edges(True)

currentSeeds = [g,h]
genusNum = 1
while True:
    nextGenusGraphs = next_genus(currentSeeds)
    genusNum += 1
    save(nextGenusGraphs, './genus_'+str(genusNum)+'_graphs')
    print "There are", len(nextGenusGraphs), "graphs for genus", genusNum
    currentSeeds = nextGenusGraphs
