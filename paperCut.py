from random import randrange
from sys import stdout
''' Homework 3 Problem 5iii
    P - 2dlist of paper rectangle prices at different lengths (Original should be a square)
    m - x-dimension length of paper
    c - y-dimension length of paper
    M[] - Memoization array
'''
def paper_cut(P,m,n, M=[]):
  if M==[]:
    M = [[None for _ in range(m + 1)] for _ in range(n+1)]

  if M[m][n] != None:
    return M[m][n]
  max_cut = [(m,n)]
  max_rev = P[m][n]
  for k in range(1, m//2 + 1):
    for l in range(1, n//2 + 1):
      print(M)
      #Upper Left
      UL_cut, UL_rev = paper_cut(P, k, l, M)
      #Lower Left
      DL_cut, DL_rev = paper_cut(P, m - k, l, M)
      #Upper Right
      UR_cut, UR_rev = paper_cut(P, k, n - l, M)
      #Lower Right
      DR_cut, DR_rev = paper_cut(P, m - k, n - l, M)
      if UL_rev + DL_rev + UR_rev + DR_rev > max_rev:
        max_rev = UL_rev + DL_rev + UR_rev + DR_rev
        max_cut = UL_cut + DL_cut + UR_cut + DR_cut
      M[m][n] = max_cut, max_rev
  return M[m][n]

def rand_paper_values(dimx, dimy, max_price): # {{{
  P = [ [0 for _ in range(dimy + 1)] for _ in range(dimx + 1) ]
  for x in range(1,dimx + 1):
    P[x] = P[x][:x] + sorted([ randrange(1, max_price+1) for _ in range(x, dimy + 1) ])
    for y in range(x, dimy + 1):
      P[y][x] = P[x][y]
  return P

x = 4
y = 4
print(paper_cut(rand_paper_values(x,y, 20), x, y))
