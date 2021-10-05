from random import randrange
from sys import stdout


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

'''
  Homework 3 Problem 1
  Followed Given solution for Homework2
  list - list of all cards
  maxlength- end of the list passed
  start - start index of the list passed
  card - current card index we are comparing to others
  Yes if returned is not -1, 0
'''
def nbankcards(list, start, maxlength, card):
  count = 0
  if maxlength - start == 0:
    return -1, 0
  if maxlength - start == 1:
    if list[card] == list[start]:
      return list[card], 1
    return -1, 0
  elif maxlength - start == 2:
    if (list[card] == list[start]) and (card != start):
      count += 1
    if (list[card] == list[maxlength - 1]) and (card != maxlength -1):
      count += 1
    return list[card], count
  if maxlength - start > 2:
    #L_card and R_card should = card, equality count
    L_card, L_count = nbankcards(list, start, start + ((maxlength - start) // 2), start)
    R_card, R_count = nbankcards(list, start + ((maxlength - start) // 2) + 1, maxlength, maxlength //2+1)
    if L_card == R_card and R_card != -1:
        return list[card], L_count + R_count
    elif L_card == -1:
      return list[R_card], R_count
    elif R_card == -1:
      return list[L_card], L_count
    else:
      L_card2, L_count2 = nbankcards(list, start, maxlength // 2, R_card)
      R_card2, R_count2 = nbankcards(list, maxlength // 2 + 1, maxlength, L_card)
      if L_count + R_count2 > R_count + L_count2 and R_card != -1:
        return list[R_card2], L_count + R_count2
      elif L_count + R_count2 < R_count + L_count2 and L_card2 != -1:
        return list[L_card2], R_count + L_count2
      else:
        return -1, 0



'''
  Homework 3 Problem 1
  list - list of all cards
  maxlength- end of the list passed
  start - start index of the list passed
  card - current card index we are comparing to others
'''
def nbankcards_memo(list, start, maxlength, card, M=[]):
  print(list)
  if maxlength - start == 0:
    return -1, 0
  if M==[]:
    M = [None for _ in range(len(list))]
  if maxlength - start == 1:
    if list[card] == list[start]:
      M[card] = 1
    return M[card]
  elif maxlength - start == 2:
    if (list[card] == list[start]) and (card != start):
      M[card] += 1
    if (list[card] == list[maxlength - 1]) and (card != maxlength -1):
      M[card] += 1
    return M[card]
  if maxlength - start > 2:
    #L_card and R_card should = card, equality count
    L_card, L_count = nbankcards_memo(list, start, start + ((maxlength - start) // 2), start, M)
    R_card, R_count = nbankcards_memo(list, start + ((maxlength - start) // 2) + 1, maxlength, maxlength //2+1, M)
    if L_card == R_card and R_card != -1:
        return list[card], L_count + R_count
    elif L_card == -1:
      return list[R_card], R_count
    elif R_card == -1:
      return list[L_card], L_count
    else:
      print(R_card)
      L_card2, L_count2 = nbankcards_memo(list, start, maxlength // 2, R_card, M)
      R_card2, R_count2 = nbankcards_memo(list, maxlength // 2 + 1, maxlength, L_card, M)
      if L_count + R_count2 > R_count + L_count2 and R_card != -1:
        return list[R_card2], L_count + R_count2
      elif L_count + R_count2 < R_count + L_count2 and L_card2 != -1:
        return list[L_card2], R_count + L_count2
      else:
        return -1, 0

n = 8
print(nbankcards(rand_cards(n), 0, n, 0))