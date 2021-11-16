# imports {{{
from copy import deepcopy
from itertools import permutations
from random import randrange
from sys import stdout
import math
#---------------------------------------------------------------------------}}}

class AdjList: # {{{
  # A class for the adjacency list representation of a graph.
  # Undirected graphs will have an edge (s,t) if and only if it has edge (t,s).
  # A directed graph might have edge (s,t) without having edge (t,s).

  # AdjList.adj is the actual adjacency list.
  # AdjList.rev is the adjacency list of the reverse graph
  # AdjList.directed is a bool indicating whether the graph is directed.
  # AdjList.nodes is an array of the form range(n).

  # Edges may be specified on initialization or with the add_edge method.

  # If A is an AdjList, then...
  #   - A[i] is the adjacency list for node i
  #   - len(A) is the number of nodes in the graph, *not* the number of edges
  #   - str(A) is a "nicer" version of the adjacency list. It gets run when you
  #     explicity or implicityly convert A to a string (like with print).
  # These correspond to the last 3 class methods.

  def __init__(self, num_nodes, edges = [], directed = False): # {{{
    self.nodes = list(range(num_nodes))
    self.adj = [ [] for _ in self.nodes ]
    self.rev = [ [] for _ in self.nodes ]
    self.directed = directed

    for (s,t) in edges:
      self.add_edge(s,t)

    self.sort()
  #--------------------------------------------------------------------------}}}

  def add_edge(self, s, t, try_directed = True): # {{{
  # Adds an edge (s,t). If the graph is undirected, it adds edge (t,s) as well.
    if t not in self.adj[s]:
      self.adj[s].append(t)
      self.rev[t].append(s)

    if not self.directed and try_directed:
      self.add_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}
  def del_edge(self, s, t, try_directed = True): # {{{
  # Deletes an edge (s,t) if it exists. If the graph is undirected, it deletes
  # the edge (t,s) as well.
    try:
      t_index = self.adj[s].index(t)
      del self.adj[s][t_index]
      s_index = self.rev[t].index(s)
      del self.rev[t][s_index]
    except ValueError:
      pass

    if not self.directed and try_directed:
      self.del_edge(t, s, try_directed = False)
  #--------------------------------------------------------------------------}}}

  def has_edge(self, s, t): # {{{
    return t in self.adj[s]
  #--------------------------------------------------------------------------}}}
  def has_edge_rev(self, s, t): # {{{
    return t in self.rev[s]
  #--------------------------------------------------------------------------}}}
  def is_path(self, path): # {{{
    """
    path is an array. Return True if path[i-1] -> path[i] in G for 
    0 < i < len(path) and false otherwise.
    """

    if not path:    # if path is [] or None
      return False

    for i in range(1, len(path)):
      if not self.has_edge(path[i-1], path[i]):
        return False
    return True
#----------------------------------------------------------------------------}}}
  def is_cycle(self, path): # {{{
    # in an undirected graph 1-cycles don't count
    if not self.directed and len(path) == 2:
      return False

    return self.is_path(list(path) + [path[0]])
#----------------------------------------------------------------------------}}}

  def in_degree(self, s): # {{{
    return len(self.rev[s])
  #--------------------------------------------------------------------------}}}
  def out_degree(self, s): # {{{
    return len(self.adj[s])
  #--------------------------------------------------------------------------}}}
  def degree(self, s): # {{{
    if not self.directed:
      return self.out_degree(s)

    return self.out_degree(s) + self.in_degree(s)
  #--------------------------------------------------------------------------}}}

  def sort(self): # {{{
    # Sort the adjacency lists
    for n in self.nodes:
      self.adj[n].sort()
      self.rev[n].sort()
  #--------------------------------------------------------------------------}}}
  def reverse(self): # {{{
    # returns reverse graph
    rev_adjlist = AdjList(self.numnodes, directed = self.directed)
    rev_adjlist.adj = deepcopy(self.rev)
    rev_adjlist.rev = deepcopy(self.adj)

    return rev_adjlist
  #--------------------------------------------------------------------------}}}

  def __getitem__(self, node):  # {{{
    return self.adj[node]
  #--------------------------------------------------------------------------}}}
  def __len__(self):  # {{{
    return len(self.nodes)
  #--------------------------------------------------------------------------}}}
  def __str__(self):  # {{{
    ret = ""
    for n in self.nodes:
      neighbors = [ str(i) for i in self.adj[n] ]
      ret += str(n) + ": " + " ".join(neighbors) + "\n"
    return ret[:-1]
  #--------------------------------------------------------------------------}}}
#----------------------------------------------------------------------------}}}

def bad_find_cycle(G): # {{{
  # Badly find (and return) a cycle in a directed or undirected graph. This is
  # a Theta(n*2^n) algorithm.

  # For directed graph, a 0 cycle is a loop, 1-cycles don't count. For
  # undirected, 1 cycles *do* count.
  if G.directed:
    cycle_lengths = range(len(G))
  else:
    cycle_lengths = [0] + list(range(2,len(G)))

  for cycle_len in cycle_lengths:
    # Generate all permutations of length cycle_len+1 with entries from G.nodes.
    # For each one, check if it is a cycle.
    for cycle_candidate in permutations(G.nodes, cycle_len+1):
      if G.is_cycle(cycle_candidate):
        return list(cycle_candidate)

  return None   # no cycle found
#----------------------------------------------------------------------------}}}
def randgraph_DAG(num_nodes, d=2):  # {{{
  # Generate a random DAG. Since bad_is_DAG calls bad_findCycle, this can be
  # *very* slow.

  num_edges = int( num_nodes*d )

  while True:
    G = AdjList(num_nodes, directed=True)
    for _ in range(num_edges):
      new_edge = (randrange(num_nodes), randrange(num_nodes))
      G.add_edge( *new_edge )
    if bad_find_cycle(G) == None:
      G.sort()
      return G
#----------------------------------------------------------------------------}}}
def randgraph(num_nodes, d=2, directed=False):  # {{{
  num_edges = int( num_nodes*d )

  G = AdjList(num_nodes, directed=directed)
  for _ in range(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    G.add_edge( *new_edge )
  G.sort()
  return G
#----------------------------------------------------------------------------}}}

def topological_sort(G):  # {{{
  """
  Return a topological sort of G if it exists. This should be a list of the
  vertices of G arranged in the topological order. Your algorithm should be
  *linear* in (number of vertices + number of edges).
  """
<<<<<<< Updated upstream

  return # remove in your solution
=======
  S = []
  while len(G.nodes) > 0:
    cycle = True
    for n in G.nodes:
      if G.in_degree(n) == 0:
        cycle = False
        S.append(n)
        for _ in range(len(G[n])):
          G.del_edge(n, G[n][0])#all edges are removed so 0 always eliminates one
        G.nodes.remove(n)
    if cycle == True:
      return None
        
  return S
>>>>>>> Stashed changes
#----------------------------------------------------------------------------}}}

def find_cycle_directed(G):  # {{{
  """
  Find a cycle in directed G if it exists. If one is found, return an array of
  the nodes in the cycle. If one is not found, return the python value None. For
  example, if we have a 4-cycle 1 -> 0 -> 5 -> 6 -> 1, then return [1,0,5,6] (or
  any cyclic permutation of this list). A loop 1 -> 1 is a 1-cycle and you
  should return [1]. In contrast to an undirected graph, 2-cycles such as 
  1 -> 2 -> 1 count as cycles.
  """
<<<<<<< Updated upstream

  return None   # no cycle present
=======
  S = []
  while len(G.nodes) > 0:
    cycle = True
    for n in G.nodes:
      if G.in_degree(n) == 0:
        cycle = False
        S.append(n)
        for _ in range(len(G[n])):
          G.del_edge(n, G[n][0])#all edges are removed so 0 always eliminates one
        G.nodes.remove(n)
    if cycle == True:
      return None
  if len(S) == 0:
    return None    
  return S
>>>>>>> Stashed changes
#----------------------------------------------------------------------------}}}

# Use this to check your topological_sort algorithm.
# A = randgraph_DAG(10, d=(1+5**0.5)/2)
<<<<<<< Updated upstream
# S = topological_sort(A)
# print(A)
# print(S)

# Use this to test your implementation of find_cycle_directed.
# for _ in range(10**3):
#   stdout.write("."); stdout.flush()
#   G = randgraph(randrange(25), d=(1+5**0.5)/2, directed=True)
#   C1 = find_cycle_directed(G)
#   print(C1)
#   if C1 != None and not G.is_cycle(C1):
#     print("Whoops!", G, C1)
#     break
=======
# print(A)
# S = topological_sort(A)
# print(S)

# Use this to test your implementation of find_cycle_directed.
for _ in range(10**3):
  stdout.write("."); stdout.flush()
  G = randgraph(randrange(25), d=(1+5**0.5)/2, directed=True)
  C1 = find_cycle_directed(G)
  print("C1: ",C1)
  if C1 != None and not G.is_cycle(C1):
    print("Whoops! G: ", G,"C1: ", C1)
    break
>>>>>>> Stashed changes
