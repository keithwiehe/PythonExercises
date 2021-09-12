''' Homework 3iii
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
    if L_rev + R_rev > max_rev:
      max_rev = L_rev + R_rev - c
      max_cut = L_cut + R_cut
  return max_cut, max_rev

''' Homework 3iv
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
    if L_rev + R_rev > max_rev:
      max_rev = L_rev + R_rev - c
      max_cut = L_cut + R_cut
  return max_cut, max_rev

''' Homework 3iv
    P - list of rod prices at different lengths
    m - max length of the rod
    c - cost per cut
    M - iterative list
'''
def modified_rod_cut_iterative(P, m, c):
  M = [None for _ in range(m+1)]
  for k in range(1, m+1):
    max_cut = [k]
    max_rev = P[k]
    for l in range(1, k//2 + 1):
      L_cut, L_rev = M[l]
      R_cut, R_rev = M[k-l]
      if L_rev + R_rev > max_rev:
        max_rev = L_rev + R_rev - c
        max_cut = L_cut + R_cut
    M[k] = max_cut, max_rev
  return M[m]

list = [0,1,3,3,15,8,15,18,19,19,20]
maxLength = 10
cost = 2
print(modified_rod_cut(list, maxLength, cost))
print(modified_rod_cut_memo(list, maxLength, cost))
print(modified_rod_cut_iterative(list, maxLength, cost))
