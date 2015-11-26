import networkx as nx
import matplotlib.pyplot as plot
import sys

graphLoc = sys.argv[1]
print "Drawing adjList:", graphLoc
graph = nx.read_adjlist(graphLoc)
nx.draw_networkx(graph)
plot.show()