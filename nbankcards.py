from random import randrange
from sys import stdout
''' HW3 Problem 1 9/14
  This solution works on paper as Theta(nlgn)
  The list is iterated through. 
  If index is not a match it is added to a new list. Then 
  n - (last set of matches) is the next list.

'''
def nbankcards(list, OriginalListSize, time):
  if list == []:
    return None
  #edge case
  if OriginalListSize == 1:
    return list[0]
  count = 0
  halfSize = OriginalListSize // 2
  Size = len(list)
  #remaining list is too small to be majority equality
  if halfSize > Size < OriginalListSize:
    return None
  matching = list[0]
  nextlist = []
  for x in list:
    time += 1
    if matching == x:
      print("Time: %i x: %i len(list): %i halfSize: %i OriginalListSize: %i Size %i" 
        %(time, x, halfSize, len(list), OriginalListSize, Size))
      count += 1
    if matching != x:
      nextlist.append(x)
    if count > halfSize:
      return x
  return nbankcards(nextlist, OriginalListSize, time)

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
#----------------------------------------------------------------------------}}}


def nbankcards_memo(list, time, maxlength, start, M=[]):
  if M==[]:
    M = [None for _ in range(len(list))]
  elif M[n]:
    return M[n]
  matching = list[n]
  if len(list) > 2:
    L_side = nbankcards_memo(list, time, n//2, start, M)
    R_side = nbankcards_memo(list, time, maxlength, n//2 + 1, M)
  for x in list:
    time += 1
    if matching == x:
      # print("Time: %i x: %i len(list): %i halfSize: %i OriginalListSize: %i Size %i" 
      #   %(time, x, halfSize, len(list), OriginalListSize, Size))
      count += 1
    if matching != x:
      nextlist.append(x)
    if count > halfSize:
      return x



n = 200
print(n)
print(nbankcards_memo(rand_cards(n), 0))