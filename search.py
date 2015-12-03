import networkx as nx 
import builderlib as blib
import os
import glob
import time

def bfsNoun(graph, noun):
	if noun not in graph.nodes():
		return 0

	total = graph[noun]["value"]

	arr = []

	for node in graph.nodes():
		graph.node[node]["visited"] = False

	# Append root's edges to the edge list
	for edge in graph.edges(noun):
		arr.append(edge[1])

	while len(arr) > 0:
		cur = arr.pop(0)
		
		graph.node[cur]["visited"] = True

		# add all the edges of the current node to edge list
		for edge in graph.edges(cur):
			# if the node has not been visited
			if not graph.node[edge[1]]["visited"]:
				arr.append(edge[1])

		# add the cur node's value to total
		total += graph.node[cur]["value"]

	return total

def valueSum(graph):
	total = 0

	for node in graph.nodes():
		total += graph.node[node]["value"]

	return total

def findMatchRate(graph, nouns):
	matchVal = 0

	for noun in nouns:
		matchVal += bfsNoun(graph, noun)

	return matchVal / valueSum(graph)

def main():
	# List all the avaliable graphs and their names
	baseDir = "/Users/francis/Documents/cpe480_texts/"
	graphs = {
		"Basic Materials : Oil And Gas" : baseDir + "basicmaterials/oilngasdrilling/oilngasdrilling.graph"
		"Basic Materials : Chemicals"   : baseDir + "basicmaterials/chemicals/chemicals.graph"
	}

	matchRate = {}

	currentArticleLoc = ""

	articleWords = blib.filterWords(currentArticleLoc)

	# For each graph in graphs
	for name, graphLoc in graphs.iteritems():
		# load the graph
		graph = nx.read_gml(graphLoc)
		# find the match rate
		rate = findMatchRate(graph, articleWords["NN"])
		# add match rate to the match rate dictionary
		matchRate[name] = rate

	# Find highest and print Match Rate
	highest = ("", 0)
	for name, rate in matchRate.iteritems():
		if rate > highest[1]:
			highest = (name, rate)

		print name, ":", rate

	print "Matched to", highest[0], ": Match Rate", highest[1]


main()