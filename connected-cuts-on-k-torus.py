import networkx as nx

G = nx.MultiGraph()
# k = raw_input("Enter genus: ")
k = 4

G.add_node(1)

print G.nodes()
print G.edges()




WHAT DO WE NEED FROM GRAPH CLASS?
- we need to add nodes
- we need to add edges w/ labels
- get edges
- get nodes
- for each edge, ask for incident vertices
- get next edge in vertex''s cyclic ordering
- 