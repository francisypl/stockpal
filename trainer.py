import networkx as nx
import builder
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
	significant = builder.filterWords(path)

	for noun in significant["NN"]:
		try:
			node = graph.node[noun]

			if posReinforce:
				node["value"] += 1
			else:
				node["value"] -= 1
		except:
			continue

# Delete nodes with a value lower than or equal to the value
def prune(graph, value):
	for node in graph.nodes():
		if node["value"] <= value:
			del node

def main():
	# baseDir = base directory of sub sector
	baseDir = "/Users/francis/Documents/cpe480_texts/basicmaterials/oilngasdrilling/"
	# graphLoc = location of edgelist
	graphName = "oilngasdrilling.graph"

	# graph = load edgelist
	graph = nx.read_adjlist(baseDir + graphLoc)

	# Get all article names in posdir
	os.chdir(baseDir + "positive")
	posArticles = glob.glob("*.txt")
	# for each article in posArticles
	for article in posArticles:
		print "[Positive] Begin", article, "...."
		start = time.time()
		reinforce(graph, article, true)
		print "Time Elapsed:", time.time() - start

	# Get all article names in negdir
	os.chdir(baseDir + "negative")
	negArticles = glob.glob("*.txt")
	# for each article in negArticles
	for article in negArticles:
		print "[Negative] Begin", article, "...."
		start = time.time()
		reinforce(graph, article, false)
		print "Time Elapsed:", time.time() - start

	# Prune the graph
	prune(graph, 2)

	# Write the graph back to edgelist
	os.chdir(baseDir)
	nx.write_adjlist(graph, graphName)

main()