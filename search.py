import networkx as nx 
import builderlib as blib
import os
import glob
import time

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