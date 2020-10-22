import os, csv
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_node('Kabir')
G.add_node('Sex')
G.add_edge('Kabir', 'Sex')

nx.draw_spectral(G, with_labels = True, node_size = 3000)
plt.show()