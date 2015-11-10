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
def filterWords(line):
	words = {"JJ": [], "NN": []}

	f = open(name,'r')
	for line in f:
		tokens = nltk.word_tokenize(removeNonAscii(line))
		tags = nltk.pos_tag(tokens)
		
		res = tagsFilter(tags)

		words["JJ"].extend(res[0])
		words["NN"].extend(res[1])

	return words

# Generate an edge list to connect source to toNodes
def edgeListFrom(source, toNodes=[]):
	edgeList = []
	for node in toNodes:
		if source is not node:
			edgeList.append((source, node))

	return edgeList

# Adds the node to the graph if the node is not in the graph
# else it increases the node's value
def addNodeToGraph(node, graph):
	if node in graph.nodes():
		graph.node[node]['value'] += 1
	else:
		graph.add_node(node, value=1)

# Return an array of the list of synsets' names
def synsetNames(synsets):
	arr = []
	for synset in synsets:
		arr.append(synset.name())
	return arr

# Add synsets and its hypernyms to the graph
def addToGraph(synsets, graph):
	# Add all the synsets to the graph
	for synset in synsets:
		addNodeToGraph(synset.name(), graph)
		
	# connect all the synsets toegether
	for synset in synsets:
		edgeList = edgeListFrom(synset.name(), toNodes=synsetNames(synsets))
		graph.add_edges_from(edgeList)

	# Add all the synsets's hypernyms to the graph
	for synset in synsets:
		hypernyms = synset.hypernyms()

		for hypernym in hypernyms:
			addNodeToGraph(hypernym.name(), graph)

		# Then connect them
		edgeList = edgeListFrom(synset.name(), toNodes=synsetNames(hypernyms))
		graph.add_edges_from(edgeList)

# Translate nouns in the document to synsets and adds them to the graph
def handleDocumentNouns(nouns, graph):
	# For each noun in nouns
	for noun in nouns:
		# Get its synsets
		synsets = wn.synsets(noun)
		# If synsets exist
		if len(synsets) > 0:
			# Add synsets and hypernyms to the graph
			addToGraph(synsets, graph)
		else:
			# search wikipedia summary, two sentences
			try:
				summary = wiki.summary(noun, sentences=2)
				# get the nouns from the summary
				tokens = nltk.word_tokenize(summary)
				tags = nltk.pos_tag(tokens)
				summaryNouns = tagsFilter(tags)[1]
				# For each noun in nouns
				for noun in summaryNouns:
				# If the noun have synsets
					synsets = wn.synsets(noun)
					if len(synsets) > 0:
					# Add synsets and hypernyms to the graph
						addToGraph(synsets, graph)
			except:
				# If we can't find the term on wikipedia, skip it
				continue

# def main():
# 	print "fileName"
# 	fileName = raw_input()
# 	significant = filterWords(fileName)

# 	graph = nx.Graph()
# 	handleDocumentNouns(significant["NN"], graph)
# 	# sentiment = determineSemtiment(significant[0])


# main()