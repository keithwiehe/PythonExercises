from random import randrange
from sys import stdout
#---------------------------------------------------------------------------}}}
def rand_rod_prices(length, max_price): # {{{
  return [0] + [ randrange(1, max_price+1) for _ in range(length) ]
#----------------------------------------------------------------------------}}}
def rand_perm(size):  # {{{
  p = []
  while len(p) < size:
    r = randrange(size)
    if r not in p:
      p.append(r)
  return p
#----------------------------------------------------------------------------}}}
def rand_cards(n, max_value=2):  # {{{
  base = []
  for value in range(1,max_value):
    max_reps = n//2 - len(base) - 1 + (n % 2)
    if max_reps == 0:
      break
    base += [value]*randrange(1,max_reps+1)
  base += [max_value]*(n-len(base))

  perm = rand_perm(n)
  base_perm = [ base[perm[i]] for i in range(n) ]

  return base_perm

def rand_paper_values(dimx, dimy, max_price): # {{{
  P = [ [0 for _ in range(dimy + 1)] for _ in range(dimx + 1) ]
  for x in range(1,dimx + 1):
    P[x] = P[x][:x] + sorted([ randrange(1, max_price+1) for _ in range(x, dimy + 1) ])
    for y in range(x, dimy + 1):
      P[y][x] = P[x][y]
  return P
#----------------------------------------------------------------------------}}}
def parts(n, I=1): # {{{
  yield (n,)
  for i in range(I, n//2 + 1):
    for p in parts(n-i, i):
      yield (i,) + p
#----------------------------------------------------------------------------}}}

def credit_card(L): # {{{
  """
  Detect whether there is an element of L that occurs more than half the time.
  You should return the element if there is one as well as a count of the number
  of times it occurs in L. If there is no such element, return None, 0.
  """

  return None, None  # remove in your solution
#----------------------------------------------------------------------------}}}

def credit_card_linear(L, recurse=True): # {{{
  return None, None  # remove in your solution
#----------------------------------------------------------------------------}}}

def paper_cut(P, dimx, dimy, M=[]): # {{{
  return ([], 0)    # remove in your solution
#----------------------------------------------------------------------------}}}
def brute_force_modified_rod_cut(P,n):  # {{{
  max_profit = float("-inf")
  for p in parts(n):
    new_profit = sum( [P[i] for i in p] ) - 2*len(p) + 2
    if new_profit > max_profit:
      max_profit = new_profit
      max_cuts = list(p)
  return max_cuts, max_profit
#-----------------------------------------------------}}}
''' Homework 3 Problem 3 iii
    P - list of rod prices at different lengths
    m - max length of the rod
    c - cost per cut
'''
def modified_rod_cut(P,m, c):
  max_cut = [m]
  max_rev = P[m]
  for l in range(1, m//2 + 1):
    L_cut, L_rev = modified_rod_cut(P,l, c)
    R_cut, R_rev = modified_rod_cut(P, m - l, c)
    if L_rev + R_rev - c> max_rev:
      max_rev = L_rev + R_rev - c
      max_cut = L_cut + R_cut
  return max_cut, max_rev

''' Homework 3 Problem 3 iv
    P - list of rod prices at different lengths
    m - max length of the rod
    c - cost per cut
    M - memoization list
'''
def modified_rod_cut_memo(P,m,c, M=[]):
  if M==[]:
    M= [None for _ in range(m+1)]
  elif M[m] != None:
    return M[m]
  max_cut = [m]
  max_rev = P[m]
  for l in range(1, m//2 + 1):
    L_cut, L_rev = modified_rod_cut_memo(P,l, c, M)
    R_cut, R_rev = modified_rod_cut_memo(P, m - l, c, M)
    if L_rev + R_rev - c> max_rev:
      max_rev = L_rev + R_rev - c
      max_cut = L_cut + R_cut
  M[m] = max_cut, max_rev
  return M[m]

''' Homework 3 Problem 3 iv
    P - list of rod prices at different lengths
    m - max length of the rod
    c - cost per cut
    M - iterative list
'''
def modified_rod_cut_iterative(P, m, c):
  M = [None for _ in range(m+1)]
  for k in range(1, m + 1):
    max_cut = [k]
    max_rev = P[k]
    for l in range(1, k//2 + 1):
      L_cut, L_rev = M[l]
      R_cut, R_rev = M[k-l]
      if L_rev + R_rev - c> max_rev:
        max_rev = L_rev + R_rev - c
        max_cut = L_cut + R_cut
    M[k] = max_cut, max_rev
  return M[m]



cost = 2
# Use this to test your various modified_rod_cut(...) functions.
## Use this to test your various modified_rod_cut(...) functions.
for _ in range(10**4):
 stdout.write(".")
 stdout.flush()
 n = randrange(2, 20)
 P = rand_rod_prices(n, 20)
 C0, R0 = brute_force_modified_rod_cut(P, n)
 C1, R1 = modified_rod_cut(P, n, cost)
 C2, R2 = modified_rod_cut_memo(P, n, cost)
 C3, R3 = modified_rod_cut_iterative(P, n, cost)
 if not (R0 == R1 == R2 == R3):
   print("Whoops!")
   print(P)
   print(C0, R0)
   print(C1, R1)
   print(C2, R2)
   print(C3, R3)
   break

