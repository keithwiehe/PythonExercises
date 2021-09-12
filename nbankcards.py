import random
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

#really slow b/c of list.pop
def nbankcards2(list, OriginalListSize, time, warning = 0):
  if list == []:
    print("WARNINGS: %i " %warning)
    return None
  #edge case
  if OriginalListSize == 1:
    print("WARNINGS: %i " %warning)
    return list[0]
  countT = 1
  countF = 0
  halfSize = OriginalListSize // 2
  Size = len(list)
  if halfSize > Size < OriginalListSize:
    print("WARNINGS: %i " %warning)
    return None
  matching = list.pop()
  #for loop starts at end of list so that list.pop() is O(1)
  for i in range(Size - 2, -1, -1):
    time += 1
    if matching == list[i]:
      print("Time: %i match: %i len(list): %i halfSize: %i OriginalListSize: %i Size %i" 
        %(time, matching, len(list), halfSize, OriginalListSize, Size))
      countT += 1
      list.pop(i)
      if i < len(list) // 10:
        warning += len(list) - i
    #not True
    else: #matching != list[i]:
      countF += 1
    if countT > halfSize:
      print("WARNINGS: %i " %warning)
      return matching
    if countF >= halfSize:
      print("WARNINGS: %i " %warning)
      return nbankcards2(list, OriginalListSize, time, warning)

nlist = list(range(1, 50000))
for i in range(0, 120):
  nlist = nlist + list(range(1, 50))
  for k in range(0,50):
    nlist.insert(random.randint(0,len(nlist) - 1),18)
nlength = len(nlist)



print(nlist)
print(nbankcards(nlist, nlength, 0))

def nbankcards3(list, OriginalListSize, time):
  print("time: %i listSize: %i" %(time, len(list)))
  time += 1
  halfOLSize = OriginalListSize // 2
  Size = len(list)
  if halfOLSize > Size < OriginalListSize:
    return None
  x = list[0]
  list.remove(x)#only pops FIRST of element
  print("x: %i halfOLSize: %i len(list): %i OriginalListSize: %i Size %i" %(x, halfOLSize, len(list), OriginalListSize, Size))
  if Size - len(list) > halfOLSize:
    return x
  nbankcards3(list, OriginalListSize, time)