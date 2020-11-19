import os, csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
""" use nested lists (n lists with n elements to represent rows and columns) as a way of representing the adjacency matrix used to put out network.
n should be probably around 500-ish and 'hits' only account for in-network accounts"""

def makeNetworkList():
	''' tells you which accounts are 'in-network'. Accounts are considered in-network 
jjjj
if they are accounts of American congresspeople or select think tanks.'''
	ls = []
	filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs' 
	for i in os.listdir(filepath): # returns tuple with index 2 value being a list
		content = i[:(len(i)-len('tweets.csv'))]
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
	counter = 0
	
	filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'
	if ls == None:
		print("Call makeNetworkList() function on a valid directory")
		return
	for i in os.listdir(filepath): # returns tuple with index 2 value being a list
		pathAndName = filepath + "/" + str(i)
		user = str(i)
		if ('.csv' in user):
			with open(pathAndName, "r") as f:
				innerdict = {}
				reader = csv.reader(f, delimiter=',')
				for i in reader:	
					counter += 1
					try:	
						if 'RT @' in i[4] and (i[4].split(' ')[1][:len(i[4].split(' ')[1]) - 1]) in ls:
							try:
								adj[user[:(len(user)-len('tweets.csv'))]][i[4].split(' ')[1][:len(i[4].split(' ')[1]) - 1]] += 1
							except KeyError: 
								print(user[:(len(user)-len('tweets.csv'))])
					except IndexError:
						print("IndexError handling this Tweet.")

	return adj

		# with open(pathAndName, 'r') as f:
		# 	df = pd.read_csv(f)
		# 	for row in df:
		# 		for column in df[row]:
					

print(makeAdjMatrix(makeNetworkList()))

# G = nx.complete_graph(20)

# # nx.draw(G)

# # plt.show()

# A = nx.to_numpy_matrix(G)

# H = nx.from_numpy_matrix(A)

# nx.draw(H)

# plt.show()