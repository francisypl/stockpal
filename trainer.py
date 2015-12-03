import networkx as nx
import builderlib as blib
import os
import glob
import time

# 
# This program reads an associative network and trainer articles
# to give positive and negative reinforments to the nodes in the
# associative network.
# 

# Reads the path of the article and either postive or negatively
# reinforces the nodes in the graph
def reinforce(graph, path, posReinforce):
	significant = blib.filterWords(path)

	for noun in significant["NN"]:
		try:
			node = graph.node[noun]

			if posReinforce:
				node["value"] += 1
			else:
				node["value"] -= 1
		except:
			continue

def averageValue(graph):
	sumVal = 0

	for node in graph.nodes():
		sumVal += graph.node[node]["value"]

	return sumVal // len(graph.nodes())

# Delete nodes with a value lower than the value
def prune(graph, value):
	for node in graph.nodes():
		if graph.node[node]["value"] < value:
			graph.remove_node(node)

def main():
	# baseDir = base directory of sub sector
	baseDir = "/Users/francis/Documents/cpe480_texts/basicmaterials/chemicals/"
	# graphLoc = location of edgelist
	graphName = "chemicals.graph"

	# graph = load edgelist
	graph = nx.read_gml(baseDir + graphName)

	# Get all article names in posdir
	print "Begin positive..."
	os.chdir(baseDir + "positive")
	posArticles = glob.glob("*.txt")
	# for each article in posArticles
	count = 1
	for article in posArticles:
		print "Reinforceing", count, "of", len(posArticles),"-", article
		start = time.time()
		reinforce(graph, article, True)
		print "Time Elapsed:", time.time() - start
		print
		count += 1

	# Get all article names in negdir
	os.chdir(baseDir + "negative")
	negArticles = glob.glob("*.txt")
	count = 1
	print "Begin negative..."
	# for each article in negArticles
	for article in negArticles:
		print "Reinforceing", count, "of", len(posArticles),"-", article
		start = time.time()
		reinforce(graph, article, False)
		print "Time Elapsed:", time.time() - start
		print
		count += 1

	# Prune the graph
	print "Pruning begins..."
	avgVal = averageValue(graph)
	print "Graph have", len(graph.nodes()), "nodes"
	prune(graph, avgVal)
	print "After prunning, graph have", len(graph.nodes()), "nodes"

	# Write the graph back to edgelist
	os.chdir(baseDir)
	nx.write_gml(graph, graphName)

main()