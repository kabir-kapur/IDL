import os, csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
# from networkx.drawing.nx_agraph import graphviz_layout

""" use nested lists (n lists with n elements to represent rows and columns) as a way of representing the adjacency matrix used to put out network.
n should be probably around 500-ish and 'hits' only account for in-network accounts"""

def makeNetworkList(filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'):
	''' tells you which accounts are 'in-network'. Accounts are considered in-network 

if they are accounts of American congresspeople or select think tanks.'''
	ls = []
	for i in list(os.listdir(filepath)): # returns tuple with index 2 value being a list
		content = i[:(len(i)-len('tweets.csv'))] # assuming the directory follows my pesonal naming convention for theese files
		if '@' in content and 'tweets' in i: # only congressional accounts have '@' in the name as per my nomenclature choices
			ls.append(content)
	if len(ls) == 0:
		ls = None
	return ls # return congressional accounts and thinkTanks list


def makeAdjMatrix(ls = None):
	'''array representation -- rows: account itself ('from') columnns: rt account ('to') 
	intersection: weight of connection (number of times from rtd to'''
	row = {rt_acct : 0 for rt_acct in ls}
	adj = {acct : row for acct in ls} # master dict
	count = 0
	innercount = 0
	
	filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'
	if ls == None:
		print("Call makeNetworkList() function on a valid directory")
		return
	for i in list(os.listdir(filepath)): # returns tuple with index 2 value being a list
		pathAndName = filepath + "/" + str(i)
		user = str(i)
		count += 1
		if ('.csv' in user):
			with open(pathAndName, "r") as f:
				innerdict = {}
				reader = csv.reader(f, delimiter=',')
				for j in reader:	
					innercount += 1
					try:	
						if 'RT @' in j[4] and (j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]) in ls:
							try:
								adj[user[:(len(user)-len('tweets.csv'))]][j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]] += 1
							except KeyError: 
								print(user[:(len(user)-len('tweets.csv'))])
					except IndexError:
						print("IndexError handling " + i + "!")
	return adj


# def makeCytoscapeList(ls = None):
# 	'''make a list of dicts that is compatible with dash - cytoscape 
# 	for application creation'''
# 	elements = []
# 	quad1x = range(0, 1)
# 	quad1y = range(0, 1)
# 	quad2x = range(0, -1)
# 	quad2y = range(0, 1)
# 	quad3x = range(0, -1)
# 	quad3y = range(0, -1)
# 	quad4x = range(0, 1)
# 	quad4y = range(0, -1)
# 	filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'
# 	count = 0
# 	innercount = 0

# 	for i in list(os.listdir(filepath)):
# 		pathAndName = filepath + "/" + str(i)
# 		user = str(i)
# 		count += 1 
# 		for j in reader:
# 			innercount += 1
# 			try:
# 				if 'RT @' in j[4] and (j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]) in ls:
# 					try:
# 						elements.append({user : {'id' : user, 'label' : user}, position : {'x' : uniform(400), 'y' : uniform(400)}})
# 						[user[:(len(user)-len('tweets.csv'))]][j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]] += 1			



def makePartiesDict(inputList = makeNetworkList()):
	'''use manual input to create a dictionary to record party affiliation.
	The Dictionary: 
	keys -- account handles
	values -- party affiliation/status as thinktank
	Since the function requires manual input, the user is expected to keep track of the dictionary on their own accord'''
	outputDict = {}
	possibilities = ['r', 'd', 'i', 't']
	try:	
		print("Would you like to skip to a certain index? y/n")
		skip = input()
		if skip == "y":
			print("Enter key: ")
			skipAcct = input()
			i = inputList.index(skipAcct)
		elif skip == "n":
			i = 0
		while i < len(inputList):
			print("Enter party abbreviation for " + inputList[i] + ", or enter undo, redo, or print: ")
			val = input()
			if val == "redo" or val == "redo ":
				i -= 1
			elif val == "skip" or val == "undo ":
				i += 1
			elif val == "print" or val == "print ":
				print(outputDict)
				print("Next index: " + inputList[i+1])
			elif val in possibilities:
				outputDict[inputList[i]] = val
				i +=1
			else:
				print("Invalid input! Try again.")
	except KeyboardInterrupt:
		print(outputDict)
		return(outputDict)
	print(outputDict)
	return outputDict

	# for i in makeNetworkList():
	# 	print("Enter party abbreviation: ")
	# 	 val = input()
	# 	 if val in possibilities:
	# 	 	outputDict[i] = val
	# 	 else:
	# 	 	print("Invalid input! Try again: ")
	# 	 	continue
		 	


					
def makeDiGraph(adjacencyMatrix = None):
	G = nx.DiGraph() # DiGraph is a directed graph with looping
	for i in adjacencyMatrix:
		G.add_node(i)
	for i in adjacencyMatrix:
		for j in adjacencyMatrix[i]:
			if adjacencyMatrix[i][j] > 0:
				G.add_edge(i, j, weight = adjacencyMatrix[i][j])
	# nx.nx_agraph.graphviz_layout(G, prog = 'my_shit') # need pygraphviz and that is a whole ordeal
	plt.figure(figsize = (20,20))
	nx.draw_circular(G)
	plt.show()

# print(makeAdjMatrix(makeNetworkList()))
# makeDiGraph(makeAdjMatrix(makeNetworkList()))


# print(makeAdjMatrix(makeNetworkList()))



# G = nx.complete_graph(20)

# # nx.draw(G)

# # plt.show()

# A = nx.to_numpy_matrix(G)

# H = nx.from_numpy_matrix(A)

# nx.draw(H)

# plt.show()
