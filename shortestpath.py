# imports {{{
from collections import deque
from heapq import heapify, heappop, heappush
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
    # rev_adjlist.adj = deepcopy(self.rev)
    # rev_adjlist.rev = deepcopy(self.adj)

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
class UnionFind:  # {{{
  # The union find (aka disjoint set) data structure. We use the straightforward
  # rank and path compression technique, but use a dictionary as the backing
  # structure.
  #
  # UnionFind.objects --- The dictionary backing. Keys are the elements, and
  #                       objects[key] is a dictionary whose keys are elements
  #                       in the same set as key with values None (value is
  #                       unimportant).
  # UnionFind.count   --- The number of disjoint sets.
  #
  # UnionFind.__init__()     --- Takes optional initial parameter listing
  #                              disjoint elements.
  # UnionFind.insert(x)      --- Insert x as a disjoint element.
  # UnionFind.insert_many(A) --- Insert elements of A as disjoint elements.
  # UnionFind.find(x)        --- Return a unique memory ID identifying the set x
  #                              belongs to. Raise an exception if x doesn't
  #                              belong to a set.
  # UnionFind.union(x,y)     --- Union the set that x belongs to with the set
  #                              that y belongs to. Will raise an exception if x
  #                              or y isn't contained in any set.
  # UnionFind.__len__()      --- Returns count, the number of disjoint sets.
  # UnionFind.__str__()      --- Nice string representation. Gets called when
  #                              cast implicitly or explicitly to a string.

  def __init__(self, A=[]): # {{{
    self.objects = dict()
    self.count = 0
    for a in A:
      self.insert(a)
  #--------------------------------------------------------------------------}}}
  def insert(self, x):  # {{{
    if not x in self.objects:
      self.objects[x] = set([x])
      self.count += 1
  #--------------------------------------------------------------------------}}}
  def find(self, x):  # {{{
    if not x in self.objects:
      raise KeyError
    return id(self.objects[x])
  #--------------------------------------------------------------------------}}}
  def union(self, x, y):  # {{{
    if self.find(x) != self.find(y):
      lx = len(self.objects[x])
      ly = len(self.objects[y])
      if lx > ly:
        x, y = y, x
      self.objects[y].update(self.objects[x])
      for z in self.objects[y]:
        self.objects[z] = self.objects[y] 
      self.count -= 1
  #--------------------------------------------------------------------------}}}
  def __len__(self):  # {{{
    return self.count
  #--------------------------------------------------------------------------}}}
  def __str__(self):  # {{{
    out = dict()
    for x in self.objects:
      out[id(self.objects[x])] = str(list( self.objects[x] ))
    return ', '.join( out.values() )
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

  def pop(self, incl_key=False):  # {{{
    # Raises exception if heap is empty
    # Get what we think the top of the heap is as a (key, value) pair. The
    # key that the dict holds should match, otherwise the key is outdated and
    # we should get the next item in the heap.

    key, value = heappop(self._heap)
    while value not in self or self[value] != key:
      key, value = heappop(self._heap)
    del self[value]
    if incl_key:
      return value, key
    return value
  #--------------------------------------------------------------------------}}}
  def peek(self, incl_key=False): # {{{
    # Raises exception if heap is empty.
    # See PriorityDict.pop for a description of what's going on.

    key, value = self._heap[0]
    while value not in self or self[value] != key:
      heappop(self._heap)   # only throws away outdated (key, value) pairs
      key, value = self._heap[0]
    if incl_key:
      return value, key
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
  def has_key(self, key):
    return super(PriorityDict, self).has_key(key)
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
def subgraph_weight(H, w):  # {{{
  return sum([ w[(u,v)] for u in H.nodes for v in H[u] ]) // 2
#----------------------------------------------------------------------------}}}
def MST_Kruskal(G,w):  # {{{
  U = UnionFind(G.nodes)
  edges_sorted = sorted( [ (u,v) for u in G.nodes for v in G[u] ], key=lambda x: w[x] )
  M = AdjList(len(G))

  for (u,v) in edges_sorted:
    if U.find(u) != U.find(v):
      U.union(u,v)
      M.add_edge(u,v)
  return M
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

def MST_Prim(G,w,s):  # {{{ w = weights s= alpha node
  Q = PriorityDict()
  pred = []
  for g in G.nodes:
    if g == s:
      Q.push(s,0)
    else:
      Q.push(g,float('inf'))
    pred.append(None)
  H = AdjList(len(G))
  print("Q list")
  while len(Q) > 0:
    u = Q.pop()
    if pred[u] != None:
      H.add_edge(pred[u], u)
    for v in G[u]:
      if v in Q and w[u,v] < Q.peek(v)[1]:
        pred[v] = u
        Q.update_key(v, w[u,v])
  return H

  # return None   # remove in your solution
#----------------------------------------------------------------------------}}}

def BellmanFord(G,w,s): # {{{
  """
  The Bellman-Ford algorithm computes shortest paths from s to g for each g in
  G. Negative weights are permitted, and the graph G is taken to be directed. G
  is assumed to not have negative cycles, and if it does the algorithm will
  detect this.

  If G contains negative cycles, return False, False. If G does not have any
  negative cycles, then return the shortest paths tree (or a list of
  predecessors) and an array of distances.
  """

  pred = [ None for _ in G.nodes ]
  dist = [ float("inf") for _ in G.nodes ]
  dist[s] = 0
  for _ in range(0, len(G)):
    for u in G.nodes: 
      for v in G[u]:
        if dist[v] > dist[u] + w[u,v]:
          dist[v] = dist[u] + w[u,v]
          pred[v] = u
    for u in G.nodes: 
      for v in G[u]:
        if dist[v] > dist[u] + w[u,v]:
          return False, False
  return pred, dist
#----------------------------------------------------------------------------}}}

# Use this to test your implementation of Prim's algorithm.
# for _ in range(10**3):
  # stdout.write("."); stdout.flush()
  # G, w = randgraph_weighted(randrange(5,25), d=(1 + 5**0.5)/2)
  # K = MST_Kruskal(G, w)
  # P = MST_Prim(G, w, 0)
  # if subgraph_weight(K, w) != subgraph_weight(P, w):
  #   print("Whoops!", G, w, K, P, sep="\n----\n")
  #   break

# Use this to test your implementation of the Bellman-Ford algorithm.
# for _ in range(10**2):
#   stdout.write("."); stdout.flush()
#   G, w = randgraph_weighted(randrange(5,25), d=(1 + 5**0.5)/2, directed=True, wt_min=-10, wt_max=10)
#   s = randrange(len(G))
#   dist1 = bad_shortest_path(G, w, s)
#   _, dist2 = BellmanFord(G, w, s)
#   if dist1 != dist2:
#     print("Whoops!", G, w, s, dist1, dist2, sep="\n----\n")
#     break

G, w = randgraph_weighted(10, d=1+5**0.5/2)
print(G,"\n-------------\n", w)