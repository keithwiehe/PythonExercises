''' Problem 3
  This solution works on paper as O(nlgn)
  The list is iterated until more than half the list matches or that is impossible. 
  Popping already existing matches as it goes. So in the next iteration 
  n - (last set of matches) is gone.

'''
def nbankcards(list, OriginalListSize):
  countT = 0
  countF = 0
  halfOriginalList = OriginalListSize // 2
  if(len(list) < halfOriginalList):
    return False
  matchList = []
  matchList.append(list[0])
  matching = list.pop()
  print("matching: %i" %(matching))#test print
  i = 0

  while True:
    print("i: %i" %(i)) #test print
    if countT >= halfOriginalList:
      return True
    if matching == list[i]:
      print("matching == true")#test print
      countT += 1
      matchList.append(list.pop([i]))
    #not True
    if matching != list[i]:
      print("countF: %i" %(countF))#test print
      countF += 1
      i += 1
    if countF >= halfOriginalList:
      return nbankcards(list, OriginalListSize)


nlist = [1,1,1,1,1,2,3,4]
nlength = len(nlist)
nbankcards(nlist, nlength)