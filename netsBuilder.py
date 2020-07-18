import networkx as nx
import numpy as np
import random

def ErdosRenyi(final_nodes, density):
  """
  This function create an Erdos-Renyi graph model

  INPUT:
    final_nodes: integer, number of graph nodes
    density: float between 0 and 1, a float near to 1 builds a graph more dense
  OUTPUT:
    G: networkx directed graph, a graph object based on Erdos-Renyi model
  """
  
  G = nx.DiGraph() #build graph

  for i in range(final_nodes): # add nodes
    G.add_node(i)

  for f in range(final_nodes): # add edges
    for j in range(final_nodes):
      if np.random.choice([0,1],p=[1 - density, density]) == 1: # the bigger density is more edges are created
        G.add_edge(f, j)
  
  return G



def WattsStrogatz(final_nodes,b_parameter, k_neighbors):
  """
  This function create an Watts-Strogatz graph model
  * It is important to emphisize that this models differs from the original one by constructing a directed graph

  INPUT:
    final_nodes: integer, final number of graph nodes (after construction)
    b_parameter: float between 0 and 1, probability of rewiring an existing edge 
    k_neighbors: integer, number of neighors a nodes that a node will link
  OUTPUT:
    G: networkx directed graph, a graph object based on Barabasi-Albert model
  """

  G = nx.DiGraph()

  for i in range(final_nodes):  # add nodes
    G.add_node(i)

  for i in range(final_nodes): # add first edges
    for k in range(int(k_neighbors/2)):
      if (i+k) < final_nodes:
        G.add_edge(i, i+k) # link the half neighbors from the right
        G.add_edge(i, abs(i-k)) # link the half neighbors from the left

  for i in range(final_nodes):
    neighbors = [n for n in G[i]] # neighbors of i
    for j in neighbors:
      if np.random.choice([0,1],p=[1-b_parameter,b_parameter]) == 1: # rewire edges with b_parameter probability
        G.remove_edge(i, j)
        G.add_edge(i, random.randrange(final_nodes))

  return G  



def  BarabasiAlbert(init_nodes,final_nodes,m_parameter):
  """
  This function create an Barabasi-Albert graph model

  INPUT:
    init_nodes: integer, initial number of nodes of the graph (before construction)
    final_nodes: integer, final number of graph nodes (after construction)
    m_parameter: integer, number of new edges added to the graph with each new node
  OUTPUT:
    G: networkx directed graph, a graph object based on Barabasi-Albert model
  """
  
  G = nx.DiGraph() # build graph

  for i in range(init_nodes): # add first nodes
    G.add_node(i)

  count = 0
  new_node = init_nodes

  for f in range(final_nodes - init_nodes):
    G.add_node(init_nodes + count) # add final nodes
    count += 1
    for e in range(0, m_parameter):
        add_edge(G,new_node, 1) # add edges
    new_node += 1
 
  return G  



def add_edge(DG,new_node, times):
  """
  Auxiliary function to add nodes in the Barabasi-Albert graph
 
  INPUT:
    graph:  networkx graph
    new_node: integer, the id of the new node created
  OUTPUT:
    new_edge: tuple (node1,node1), a tuple of the 2 nodes that the new link will be created
  """
      
  if len(DG.edges()) == 0: # if the graph has no edges yet, the new node will link node '0'
      random_proba_node = 0
  else: # else, we choose an existing node based on its degree to link the new node
      nodes_probs = []  
      for node in DG.nodes():
          node_degr = DG.degree(node)
          node_proba = node_degr / (2 * len(DG.edges()))
          nodes_probs.append(node_proba)
      random_proba_node = np.random.choice(DG.nodes(),p=nodes_probs)
      
  
  new_edge = (random_proba_node, new_node)
  repeats = times + 1
  if new_edge in DG.edges(): # if the link already exists, the function is called again
    if repeats > 3:
      pass
    else:
      add_edge(DG,new_node, repeats)
  else:
      DG.add_edge(random_proba_node, new_node)
 
  return new_edge  



def  ErdosRenyiBoolEnsemble(N, size_list, density_list):
  """
  This function create an ensemble Erdos-Renyi graph models

  INPUT:
    N: int, number of networks to be created
    size_list, list of integers, a list with the size of each network to be created
    density_list: list of floats, a list with the density paramenter for each network to be created
  OUTPUT:
    ensemble: list of networkx directed graphs, a list of graph objects 
  """

  ensemble = []
  for n in range(N):
    net = ErdosRenyi(size_list[n], density_list[n])
    net = makeRandomBoolNet(net)
    ensemble.append(net)
  
  return ensemble



def  WattsStrogatzBoolEnsemble(N, size_list, b_parameter_list, k_neighbors_list):
  """
  This function create an ensemble of Watts-Strogatz graph models

  INPUT:
    N: int, number of networks to be created
    size_list, list of integers, a list with the size of each network to be created
    b_parameter_list: list of floats, a list with the b paramenter for each network to be created
    k_neighbors_list: list of integers, a list with the k neighbors for each network to be created
  OUTPUT:
    ensemble: list of networkx directed graphs, a list of graph objects 
  """

  ensemble = []
  for n in range(N):
    net = WattsStrogatz(size_list[n], b_parameter_list[n], k_neighbors_list[n])
    net = makeRandomBoolNet(net)
    ensemble.append(net)
  
  return ensemble  



def  BarabasiAlbertBoolEnsemble(N, size_list, init_nodes_list, m_parameter_list):
  """
  This function create an ensemble of Barabasi-Albert graph models

  INPUT:
    N: int, number of networks to be created
    size_list, list of integers, a list with the size of each network to be created
    init_nodes_list: 
    m_parameter_list: list of floats, a list with the m paramenter for each network to be created
  OUTPUT:  
    ensemble: list of networkx directed graphs, a list of graph objects 
  """
  
  ensemble = []
  for n in range(N):
    net = BarabasiAlbert(init_nodes_list[n],size_list[n],m_parameter_list[n])
    net = makeRandomBoolNet(net)
    ensemble.append(net)
  
  return ensemble  
