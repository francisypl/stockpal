from nltk.corpus import wordnet as wn
import networkx as nx
import nltk
import wikipedia as wiki

#
# This program reads a text file and builds a associative graph
# using the NLTK Wordnet as a base for relative terms.
# The graph will then be exported as a text file.
#

# Filter and return nouns and adjectives from tags
# Adjectives : 0, Nouns : 1
def tagsFilter(tags):
	important = {"JJ": 0, "JJR": 0, "JJS": 0, 
	             "NN": 1, "NNP": 1, "NNPS": 1, 
	             "NNS": 1}

	words = {0: [], 1: []}
	for tag in tags:
		if tag[1] in important and len(tag[0]) > 1:
			wordType = important[tag[1]]
			words[wordType].append(tag[0])

	return words

def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

# Tokenize and pos tag words then filter them 
# and return significant words
def filterWords(name):
	words = {"JJ": [], "NN": []}

	f = open(name,'r')
	for line in f:
		tokens = nltk.word_tokenize(removeNonAscii(line))
		tags = nltk.pos_tag(tokens)
		
		res = tagsFilter(tags)

		words["JJ"].extend(res[0])
		words["NN"].extend(res[1])

	return words

# Generate an edge list connect source to nodes
def edgeListFrom(source, toNodes=[]):
	edgeList = []
	for node in toNodes:
		if source is not node:
			edgeList.append((source, node))

	return edgeList

# Adds the node to the graph if the node is not in the graph
# else it increases the node's value
def addNodeToGraph(node, graph):
	if node in graph.nodes:
		graph.node[name]['value'] += 1
	else:
		graph.add_node(name, value=1)

# Build an associative network
def buildGraph(nouns):
	graph = nx.Graph()

	for noun in nouns:
		# Get a list of its synsets, pos = wn.NOUN
		synsets = wn.synsets(noun, pos=wn.NOUN)
		# If synsets exist
		if len(synsets) > 0:
			# Add all the synsets to the graph
			for synset in synsets:
				name = synset.name()
				# Add the synset to the graph
				addNodeToGraph(name, graph)
				
			# connect all the synsets toegether
			for synset in synsets:
				edgeList = edgeListFrom(synset, toNodes=synsets)
				graph.add_edges_from(edgeList)

			# Add all the synsets's hypernyms to the graph
			for synset in synsets:
				hypernyms = wn.hypernyms(synset)

				for hypernym in hypernyms:
					addNodeToGraph(hypernym.name(), graph)

				# Then connect them
				edgeList = edgeListFrom(synset, toNodes=hypernyms)
				graph.add_edges_from(edgeList)
		else:
			# Find its wikipedia summary, 2 sentences


def main():
	print "fileName"
	fileName = raw_input()
	significant = filterWords(fileName)

	# sentiment = determineSemtiment(significant[0])
	graph = buildGraph(significant["NN"])


main()