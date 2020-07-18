import networkx as nx
import numpy as np
import multiprocessing 
from contextlib import closing
import netsBuilder as nb

def makeRandomBoolNet(DG):
  """
  This function add the Boolean formalism to the network, creating random logic functions in order to perform dynamics 

  INPUT:
    G: networkx directed graph, a graph object
  OUTPUT:
    G: networkx directed graph, a graph object with logic functions in each node
  """

  for i in range(len(DG)):
     DG.nodes[i]['function'] = []
    
  for i in range(len(DG)):
    neighbors = [n for n in DG[i]]
    rule_string = []
    for j in neighbors:
        rule_string = np.random.choice(['!', ''] )
        DG.nodes[j]['function'].append(rule_string)
        DG.nodes[j]['function'].append('gene'+str(i))
        rule_string = np.random.choice(['|', '&'])
        DG.nodes[j]['function'].append(rule_string)
        rule_string = []

  for i in range(len(DG)):
    DG.nodes[i]['function'] = [''.join(x) for x in DG.nodes[i]['function']]
    
  for i in range(len(DG)):
    DG.nodes[i]['function'] = DG.nodes[i]['function'][:-1]

  return DG



def setState(net, initial_state):
  """
  This function set the states (zeros or ones) of the network
  INPUT:
    net: networkx graph
    initial_state: integer, number of generations to evolve the network
  OUTPUT:
    dynamicMatrix: numpy matrix, matrix of zeros and ones (onde axis are the nodes and the other are the discrete time points)
  """

  net_aux = net.copy()
  i = 0
  for g in list(net_aux.nodes):
    net_aux.nodes[g]['state'] = initial_state[i]
    i += 1
  
  return net_aux


def update_network_sinchronous(net):
  """
  This function update the net states based on its logical functions
  INPUT:
    net: networkx graph (before)
  OUTPUT:
    net: networkx graph (after)
  """
  net_aux = net.copy()
  for j in range(len(net)):
    state = 0
    logical = 0
    negative = 0
    init = 0
    for i in net.nodes[j]['function']:
      if i == ' ' or i =='':
        pass
      elif i == '!':
        negative = 1

      elif i == '|':
        logical = 0

      elif i == '&': 
        logical = 1

      else: 
        if init == 0:
          state = net.nodes[int(i.translate({ord(i): None for i in 'gen'}))]['state']
          init = 1
        else:
          if logical == 0 :
            if negative == 0:
              state = state or net.nodes[int(i.translate({ord(i): None for i in 'gen'}))]['state']
            else:
              state = state or abs(net.nodes[int(i.translate({ord(i): None for i in 'gen'}))]['state'] - 1)
              negative = 0
          else:
            if negative == 0:
              state = state and net.nodes[int(i.translate({ord(i): None for i in 'gen'}))]['state']
            else:
              state = state and abs(net.nodes[int(i.translate({ord(i): None for i in 'gen'}))]['state'] - 1)
              negative = 0
  
    net_aux.nodes[j]['state'] = state
      
  return net_aux




def get_network_states(net):
  """
  This function evolve the network 
  INPUT:
    net: networkx graph
  OUTPUT:
    states: list, states of the network nodes
  """

  states = []
  for node in net:
    states.append(net.nodes[node]['state'])
  return states 


def evolve(net, initial_state, generations):
  """
  This function evolve the network 
  INPUT:
    network: networkx graph
    initial_state: numpy array, beggining states of each node
    generations: integer, number of generations to evolve the network
  OUTPUT:
    dynamicMatrix: numpy array of arrays, array of arrays of zeros and ones (onde axis are the nodes and the other are the discrete time points)
  """

  
  net = setState(net, initial_state) # Set initial states

  dynamicMatrix = np.array( get_network_states(net))  # Initiate dynamic matrix

  for g in range(generations):
    net = update_network_sinchronous(net)
    dynamicMatrix = np.vstack((dynamicMatrix, get_network_states(net)))

  return dynamicMatrix




def multipleEvolution(net, initial_states, generations):
  """
  This function evolve the network from many initial states
  INPUT:
    network: networkx graph
    generations: integer, number of generations to evolve the network
    initial_states: numpy array of arrays, different initial_states of the network
  OUTPUT:
    dynamic_list: numpy array of arrays, list of dynamics from each initial state
  """

  dynamic_list = []
  for s in initial_states:
    dynamic_list.append(evolve(net, s, generations))

  return dynamic_list



def auxMultipleParallelEvolution(input): 
  """
  Auxiliar function of multipleParallelEvolution
  INPUT:
    input: list of the multipleParallelEvolution parameters
  OUTPUT:
    output of evolve functions
  """
  return evolve(input[0], input[1], input[2])


#@jit
def multipleParallelEvolution(net, initial_states, generations):
  """
  This function evolve the network from many initial states
  INPUT:
    network: networkx graph
    generations: integer, number of generations to evolve the network
    initial_states: numpy array of arrays, different initial_states of the network
  OUTPUT:
    dynamic_list: numpy array of arrays, list of dynamics from each initial state
  """

  input = [[net, s, generations] for s in initial_states]
  with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
    dynamic_list = pool.map(auxMultipleParallelEvolution, input)

  return dynamic_list


def auxEnsembleParallelEvolution(input): 
  """
  Auxiliar function of multipleParallelEvolution
  INPUT:
    input: list of the multipleParallelEvolution parameters
  OUTPUT:
    output of evolve functions
  """
  return multipleParallelEvolution(input[0], input[1], input[2], input[3])



def ensembleParallelEvolution(ensemble, nis, generations, nthreads):
  """
  This function 

  INPUT:
    ensemble:
    nis:
    generations: 
    nthreads: 
  OUTPUT:  
    results:
  """

  input2 = [[e,state_generator(nis, len(e)), generations, nthreads] for e in ensemble]
  with closing(Pool(nthreads)) as p:
    output = p.map(auxEnsembleParallelEvolution, input2)
  
  return output



def hareTortoise(states):
  """
  This function identify a cycle in an array using the "tortoise and the hare algorithm" alluding to Aesop's fable 
  INPUT:
    states: numpy array, states over discrete time points
  OUTPUT:
    mu: integer, time point where cycle begins
    lam: integer, time point where cycle ends
  """
  power = lam = 1 
  tortoise = states[0]
  tstep = 0
  hare = states[1]
  hstep = 1
  while not np.array_equal(hare, tortoise): 
    if power == lam:
      tortoise = hare
      power *=2
      lam = 0
    hstep += 1
    if(hstep >= len(states)): # check for inconsistencies
      return 1, 1 # there is no convergence
    hare = states[hstep]
    lam += 1
  
  tortoise = hare = states[0]
  hstep = 0
  for i in range(lam):
    hstep += 1
    hare = states[hstep]

  mu = 0
  while not np.array_equal(hare, tortoise):
    tstep += 1
    tortoise = states[tstep]
    hstep += 1
    hare = states[hstep]
    mu += 1

  return mu, lam



def getCycle(states):
  """
  This function returns a cycle in an array
  INPUT:
    states: numpy array, states over discrete time points
  OUTPUT:
    mu: integer, time point where cycle begins
    lam: integer, time point where cycle ends
    cycles: list of states, the states contained in the cycle
  """
  for i in range(1,len(states)):
    if np.array_equal(states[i-1], states[i]):
      cycle = states[i]
      return [i, i, cycle] # steady state
   
  lam, mu = hareTortoise(states) # get initial and final position of the cycle
  
  if lam == 1:
    return 0, 0, np.zeros(len(states[0])) # there is no convergence

  cycle = states[mu:(lam+mu)]
  return [lam, mu, cycle] # limit cycle