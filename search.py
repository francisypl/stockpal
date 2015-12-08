import networkx as nx 
from nltk.corpus import wordnet as wn
import builderlib as blib
import os
import sys
import glob
import wikipedia as wiki
import time

def bfsNoun(graph, noun):
	if noun not in graph.nodes():
		return 0

	total = graph.node[noun]["value"]

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

	count = 1
	for noun in nouns:
		sys.stdout.write("\rMatching %d of %d" % (count, len(nouns)))
		sys.stdout.flush()

		synsets = wn.synsets(noun)

		if len(synsets) == 0:
			try:
				summary = wiki.summary(noun, sentences=2)
				wikiWords = blib.tokenizeAndTag(summary)

				for wikiWord in wikiWords["NN"]:
					synsets.extend(wn.synsets(wikiWord))
			except:
				pass

		for synset in synsets:
			matchVal += bfsNoun(graph, synset.name())

		count += 1

	return matchVal / valueSum(graph)

def main():
	# List all the avaliable graphs and their names
	baseDir = "/Users/francis/Documents/cpe480_texts/"
	graphs = {
		"Basic Materials : Oil And Gas" : baseDir + "basicmaterials/oilngasdrilling/oilngasdrilling.graph",
		"Basic Materials : Chemicals"   : baseDir + "basicmaterials/chemicals/chemicals.graph"
	}

	matchRate = {}

	currentArticleLoc = "/Users/francis/Documents/cpe480_texts/unmatched/" + sys.argv[1]

	articleWords = blib.filterWords(currentArticleLoc)
	# For each graph in graphs
	begin = time.time()
	print "Begin Matching..."
	for name, graphLoc in graphs.iteritems():
		print "Matching", name, "graph..."
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

	print sys.argv[1], "..."
	print "Matched to", highest[0], ": Match Rate", highest[1]
	print "Time Elapsed:", (time.time() - begin) / 60, "mins"


main()