# imports {{{
from collections import deque
from heapq import heapify, heappush, heappop
from itertools import chain
from random import randrange
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
class PriorityDict(dict):  # {{{
  # A dictionary that maintains a heap with items in the dictionary sorted
  # according to the dictionary keys. It is a subclass of the dictionary class.
  # You can read about dictionaries here:
  #
  #   https://docs.python.org/2/library/stdtypes.html#typesmapping
  #
  # Methods from the dictionary superclass are inherited, but some might not
  # play nicely with the heap.
  #
  # Updating the keys is supported, which is the main benefit. We use a heap to
  # store the data, and a dictionary structure to store the (key, value)
  # association. Upon updating a key, we update the dictionary and add a
  # *duplicate* entry to the heap (or rebase if it has grown too large). This
  # saves O(n) on each operation until we have to rebase. When we pop from the
  # heap, we have to make sure that we're not getting a value with an outdated
  # key, so we check the dictionary to see if the keys match.
  #
  # PriorityDict._heap -- the actual heap
  #
  # PriorityDict._rebuild() -- rebuilds the heap
  #
  # PriorityDict.pop() -- returns and removes the element with the least key
  # PriorityDict.peek() -- returns and does not remove the element with the
  #   least key
  # PriorityDict.push(value,key) -- adds the (key, value) pair to the heap
  # PriorityDict.update_key(value,key) -- updates the key of value to new_key

  def __init__(self, *args, **kwargs):  # {{{
    # call the dictionary __init__ from the superclass
    super(PriorityDict, self).__init__(*args, **kwargs)
    self._rebuild()  # sets up the heap
  #--------------------------------------------------------------------------}}}
  def _rebuild(self): # {{{
    # The heap likes key to come before value, but we store it backwards in the
    # dictionary
    self._heap = [(key, value) for (value, key) in self.items()]
    heapify(self._heap)   # O(n)
  #--------------------------------------------------------------------------}}}

  def pop(self):  # {{{
    # Raises exception if heap is empty
    # Get what we think the top of the heap is as a (key, value) pair. The
    # key that the dict holds should match, otherwise the key is outdated and
    # we should get the next item in the heap.

    key, value = heappop(self._heap)
    while value not in self or self[value] != key:
      key, value = heappop(self._heap)
    del self[value]
    return value
  #--------------------------------------------------------------------------}}}
  def peek(self): # {{{
    # Raises exception if heap is empty.
    # See PriorityDict.pop for a description of what's going on.

    key, value = self._heap[0]
    while value not in self or self[value] != key:
      heappop(self._heap)   # only throws away outdated (key, value) pairs
      key, value = self._heap[0]
    return value
  #--------------------------------------------------------------------------}}}
  def push(self, value, key):  # {{{
    # adds (key,value) to heap and to the dictionary

    heappush(self._heap, (key, value))
    self[value] = key
  #--------------------------------------------------------------------------}}}
  def update_key(self, value, key): # {{{
    # Update the key for value. We don't remove it from the heap since this will
    # be O(n). Instead we update the key in the dictionary and add a duplicate
    # to the heap. If the heap is too big (2x the dictionary), then we rebuild
    # so that we aren't wasting memory.

    super(PriorityDict, self).__setitem__(value, key)
    heappush(self._heap, (key, value))

    # rebuild the heap if it's too big
    if len(self._heap) >= 2*len(self):
      self._rebuild()
  #--------------------------------------------------------------------------}}}

  def __setitem__(self, value, key):  # {{{
    self.update_key(value,key)
  #--------------------------------------------------------------------------}}}
#---------------------------------------------------------------------------}}}

def is_connected(G):  # {{{
  seen = [ False for _ in G.nodes ]
  seen[0] = True
  working_nodes = deque([0])
  while len(working_nodes) != 0:
    u = working_nodes.popleft()
    for v in G[u]:
      if not seen[v]:
        seen[v] = True
        working_nodes.append(v)

  return False not in seen
#----------------------------------------------------------------------------}}}
def randgraph_weighted(num_nodes, d=2, directed=False, wt_min=None, wt_max=None):  # {{{
  if not wt_min:
    wt_min = num_nodes // 2
  if not wt_max:
    wt_max = (num_nodes * 3) // 2

  num_edges = int( num_nodes*d )

  G = AdjList(num_nodes, directed=directed)
  while not is_connected(G):
    G = AdjList(num_nodes, directed=directed)
    w = dict()
    for _ in range(num_edges):
      (u, v) = (randrange(num_nodes), randrange(num_nodes))
      while u == v:
        (u, v) = (randrange(num_nodes), randrange(num_nodes))
      G.add_edge(u,v)
      w[u,v] = randrange( wt_min, wt_max+1 )
      while w[u,v] == 0:
        w[u,v] = randrange( wt_min, wt_max+1 )
      if not directed:
        w[v,u] = w[u,v]

  G.sort()
  return G, w
#----------------------------------------------------------------------------}}}
def paths_length(G, k, start=None): # {{{
  if k == 0:
    if start == None:
      for g in G.nodes:
        yield [g]
    else:
      yield [start]
  else:
    for path in paths_length(G, k-1, start=start):
      for v in G[path[-1]]:
        if v not in path:
          yield path+[v]
#----------------------------------------------------------------------------}}}
def all_paths(G, start=None): # {{{
  return chain.from_iterable(paths_length(G, k, start=start) for k in range(1,len(G)))
#----------------------------------------------------------------------------}}}
def bad_negative_cycle(G,w,s): # {{{
  for P in all_paths(G, start=s):
    for k in range(len(P)):
      if G.is_cycle(P[k:]):
        Q = P[k:]
        cycle_wt = sum([ w[Q[i],Q[i+1]] for i in range(len(Q)-1) ]) + w[Q[-1],Q[0]]
        if cycle_wt < 0:
          return True
  return False
#----------------------------------------------------------------------------}}}
def bad_shortest_path(G,w,s): # {{{
  if bad_negative_cycle(G,w,s):
    return False

  dist = [ float("inf") for _ in G ]
  dist[s] = 0
  for P in all_paths(G, start=s):
    path_wt = sum([ w[P[i],P[i+1]] for i in range(len(P)-1) ])
    if dist[P[-1]] > path_wt:
      dist[P[-1]] = path_wt
  return dist
#----------------------------------------------------------------------------}}}

def Dijkstra(G,w,s):  # {{{
  """
  Dijkstra's shortest path algorithm. Return the shortest paths tree M and an
  array dist such that 
    dist[u] = the distance from s to u along the unique path in M from s to u
            = the shortest distance from s to u in G
  Disregarding operations on the priority queue, your algorithm should run in
  O(m), where m is the number of edges in G.
  """

  dist = [ float("inf") for n in G.nodes ]
  M = AdjList(len(G))
  Q = PriorityDict()
  for g in G.nodes:
    if g == s:
      Q.push(s,0)
    else:
      Q.push(g,float('inf'))
  pred = [None for n in G.nodes]
  dist[s] = 0
  while len(Q) > 0:
    u = Q.pop()    
    if pred[u] != None:
      M.add_edge(pred[u], u)
    for v in G[u]:
      if v in Q and dist[v] > dist[u] + w[u,v]:
        Q.update_key(v, dist[u]+w[u,v])
        dist[v]=dist[u] + w[u,v]
        pred[v] = u
  return M, dist
#----------------------------------------------------------------------------}}}

# Use this to test your implementation of Dijkstra's algorithm.
for _ in range(100):
  stdout.write("."); stdout.flush()
  G, w = randgraph_weighted(randrange(5,25), d=(1 + 5**0.5)/2, directed=True)
  s = randrange(len(G))
  dist1 = bad_shortest_path(G, w, s)
  _, dist2 = Dijkstra(G, w, s)
  if dist1 != dist2:
    print("Whoops!", G, w, dist1, dist2, sep="\n----\n")
    break