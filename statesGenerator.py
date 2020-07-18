import numpy as np

def state_generator(n, size):
  """
  This function generates random lists of zeros and ones 
  INPUT:
    n: integer, number of lists
    size: integer, size of each list
  OUTPUT:
    states: numpy matrix, array of arrays of zeros and ones 
  """

  total_possibilities = (2 ** size) - 1 # number of all possible initial states 

  if n > total_possibilities:
    return [0] # "Number of lists exceed the number of all possible initial states"

  states = np.array([i for i in range(size)]) # build list of states
  for i in range(n):
    value = random.randint(0,total_possibilities) # randomly choose an integer in the range of all possible initial states
    state = [int(d) for d in str(bin(value))[2:]] # transform the integer to binary
    for j in range(size - len(state)): # insert zeros on the empty positions
      state.insert(0, 0)
    states = np.vstack([states,state]) # insert the new state
  states = np.delete(states, 0,0) # erase the first position of the created list of initial states


  unique_states = np.unique(states,axis=0)
  uniques = len(unique_states)

  while uniques < n:
    for i in range(n - uniques):
      value = random.randint(0,total_possibilities) # randomly choose an integer in the range of all possible initial states
      state = [int(d) for d in str(bin(value))[2:]] # transform the integer to binary
      for j in range(size - len(state)): # insert zeros on the empty positions
        state.insert(0, 0)
      unique_states = np.vstack([unique_states,state]) # insert the new state
    unique_states = np.unique(unique_states,axis=0) # select only unique initial states
    uniques = len(unique_states)
    print(uniques)

  return unique_states

