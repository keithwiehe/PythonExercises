# ID: Ochieng1, Ahng7rah, ma7EiSho, Aekizo1O
# imports {{{
from collections import deque
from copy import deepcopy
from itertools import permutations
from random import choice, randrange
from sys import stdout
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
      ispath = self.has_edge(path[i - 1], path[i])
      if not ispath:
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
      self.adj[n] = sorted(self.adj[n])
      self.rev[n] = sorted(self.rev[n])
  #--------------------------------------------------------------------------}}}
  def reverse(self): # {{{
    # returns reverse graph
    rev_adjlist = AdjList(self.numnodes, directed = self.directed)
    rev_adjlist.adj = deepcopy(self.adj)
    rev_adjlist.rev = deepcopy(self.rev)

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

def randgraph(num_nodes, d=2):  # {{{
  num_edges = int( num_nodes*d )

  G = AdjList(num_nodes)
  for _ in range(num_edges):
    new_edge = (randrange(num_nodes), randrange(num_nodes))
    if not G.has_edge( *new_edge ):
      G.add_edge( *new_edge )
  G.sort()
  return G
#----------------------------------------------------------------------------}}}
def predecessors(BFS_Tree, u, stop_at=None): # {{{
  # Return an array of predecessors of u in the BFS tree. The last element will
  # be the root, and the first will be u. If stop_at is specified, then stop at
  # that ancestor instead of the root of the tree

  preds = [u]
  parent = u
  while len(BFS_Tree.rev[parent]) != 0 and parent != stop_at:
    parent = BFS_Tree.rev[parent][0]
    preds.append(parent)
  return preds
#----------------------------------------------------------------------------}}}
def common_ancestor_paths(BFS_Tree, u, v): # {{{
  # The nodes u and v have a common ancestor, call it c. Function returns a pair
  # of arrays U, V such that U is a path in BFS_Tree from u to c and V is a path
  # in BFS_Tree from v to c.

  preds_u = predecessors(BFS_Tree, u)
  preds_v = predecessors(BFS_Tree, v)
  while len(preds_u) != 0 and len(preds_v) != 0 and preds_u[-1] == preds_v[-1]:
    common_ancestor = preds_u.pop()
    preds_v.pop()

  path_u_common_ancestor = predecessors(BFS_Tree, u, stop_at=common_ancestor)
  path_v_common_ancestor = predecessors(BFS_Tree, v, stop_at=common_ancestor)

  return path_u_common_ancestor, path_v_common_ancestor
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

def DFS(G,s): # {{{
  """
  G is an AdjList representation of a graph and s is a node in the graph. Return
  the Depth First Search tree for G and s.

  For the stack, we use the python data structure deque. It is something like a
  symmetric queue (i.e. a stack+queue), with Theta(1) operations to add/pop
  elements from either end. Read about it here:
  https://docs.python.org/3.3/library/collections.html#collections.deque
  """

  explored = [ False for _ in G.nodes ]
  seen = [ False for _ in G.nodes ]

  seen[s] = True
  DFS_Tree = AdjList(len(G), directed=True)
  working_nodes = deque([s])
  while len(working_nodes) != 0:
    u = working_nodes.pop()
    for v in G[u]:
      if not explored[v]:
        working_nodes.append(v)
      if not seen[v]:
        DFS_Tree.add_edge(u,v)
        seen[v] = True
    explored[u] = True

  return DFS_Tree
#----------------------------------------------------------------------------}}}

def BFS(G, s):  # {{{
  """
  Breadth First search for G and s. Returns a BFS tree rooted at s (in the form
  of a predecessors array, or as an AdjList  graph) and the distances array.

  For the queue, you should use the python data structure deque. It is something
  like a symmetric queue, with Theta(1) operations to add/pop elements from
  either end. Read about it here:
  https://docs.python.org/3.3/library/collections.html#collections.deque
  """
  dist = [float('inf') for _ in G.nodes]
  seen = [ False for _ in G.nodes ]

  seen[s] = True
  dist[s] = 0
  BFS_Tree = AdjList(len(G), directed=True)
  working_nodes = deque([s])
  while len(working_nodes) != 0:
    u = working_nodes.pop()
    for v in G[u]:
      if not seen[v]:
        working_nodes.append(v)
        BFS_Tree.add_edge(u,v)
        seen[v] = True
        dist[v] = dist[u] + 1
  return BFS_Tree, dist


#----------------------------------------------------------------------------}}}

def find_cycle(G): # {{{
  """
  Find a cycle in undirected G if it exists. If one is found, return an array of
  the nodes in the cycle. If one is not found, return the python value None. For
  example, if we have a 5-cycle 1 -- 0 -- 5 -- 6 -- 1, then return [1,0,5,6] (or
  any cyclic permutation of this list). A loop 1 -- 1 is a 0-cycle and you
  should return [1]. Things like 1 -- 2 -- 1 don't count as cycles since you
  have to take the same edge back to 1. 

  You might want to use the helper function common_ancestor_paths().
  didn't finish"""
  n = choice(G.nodes)
  BFS_tree, dist = BFS(G, n)#constant
  # print("n: ", n, "BFS_tree:\n",BFS_tree)
  seen = [False for _ in G.nodes]#constant
  working_nodes = deque([n])
  seen[n] = True
  while len(working_nodes) != 0:#nodes
    u = working_nodes.pop()
<<<<<<< Updated upstream
    print("length: ", len(G[u]), " G[u]: ", G[u])
    if len(G[u]) == 1:
      working_nodes.append(G[u][0])
      seen[G[u][0]] = True
    for i in range(1, len(G[u])):
      node1 = G[u][i-1]
      node2 = G[u][i]
      working_nodes.append(node1)
      print("node1: ", node1, "node2: ", node2)
      cycle = common_ancestor_paths(BFS_tree, node1, node2)
      if cycle != []:
        print("cycle: ", cycle)
        return cycle[1]#only care about second tuple
      seen[node1] = True    
=======
    for i in BFS_tree[u]:
      working_nodes.append(i)
      for k in BFS_tree[i]:
        print("u: ",u,"i: ", i, "k: ", k)
        cycle = common_ancestor_paths(BFS_tree, u, i)
        cycle2 = common_ancestor_paths(BFS_tree, i, k)
        cycle3 = common_ancestor_paths(BFS_tree, k, u)
        # cycle += cycle2 + cycle3
        print("cycle1: ", cycle,"cycle2: ", cycle2,"cycle3: ", cycle3)
        if G.is_cycle(cycle[0] + cycle[1]):
          return cycle
      seen[i] = True    
>>>>>>> Stashed changes
  print("returning None.")
  return None

  
  
#----------------------------------------------------------------------------}}}


# Use this to test your implementation of BFS
# G = randgraph(12)
# s = choice(G.nodes)
# t = s
# while s ==t:
# t = choice(G.nodes)
# T, dist = BFS(G, t)
# print("G:\n", G)
# print("t: ", t)
# print("T:\n", T)
# print(dist)
# print("s: ", s)
# S, distS = BFS(G, s)
# print("S: ", S)
# print(distS)


# Use this to test your implementation of find_cycle
for _ in range(10**3):
  stdout.write("."); stdout.flush()
  A = randgraph(randrange(25), d=(1 + 5**0.5)/2 )
  print("------------------------------------\nA creation:\n", A)
  print("end A creation")
  C = find_cycle(A)
  D = bad_find_cycle(A)
  if not ( C == None or A.is_cycle(C) ) or ( C == None and D != None ) or ( C != None and D == None):
    print("Whoops!\n A:", A,"\nC: ", C, "\nD: ", D)
    break