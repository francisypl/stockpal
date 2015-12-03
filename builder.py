import networkx as nx
import os
import glob
import time
import builderlib as blib

#
# This program reads a text file and builds a associative graph
# using the NLTK Wordnet as a base for relative terms.
# The graph will then be exported as a text file.
#

def main():
	baseDir = "/Users/francis/Documents/cpe480_texts/basicmaterials/chemicals"

	os.chdir(baseDir)
	articles = glob.glob('*.txt')

	graph = nx.Graph()
	print "Let's get to work!"
	for index in range(0, len(articles)):
		start = time.time()
		article = articles[index]

		print article, "- (",index + 1,"of", len(articles),")"

		significant = blib.filterWords(article)
		blib.handleDocumentNouns(significant["NN"], graph)
		
		print article, "done."
		print "Time Elapsed:", time.time() - start, "seconds"
		print
		print
		# sentiment = determineSemtiment(significant[0])

	# Export graph data to a file
	edgeListFile = "chemicals.graph"
	print "Writing graph to file...."
	nx.write_gml(graph, edgeListFile)
	print "done"

main()