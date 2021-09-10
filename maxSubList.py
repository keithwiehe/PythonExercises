def maxSubList(list):
  sum = 0
  maxSum = 0
  iMax = 0
  jMax = 0
  iCurrent = 0
  jCurrent = 0
  lastNeg = False
  for index, num in enumerate(list):
    if num >= 0:
      sum = sum + num
      jCurrent = index
      if(lastNeg == True):
        iCurrent = index
      if sum > maxSum:
        maxSum = sum
        iMax = iCurrent
        jMax = jCurrent
      lastNeg = False
    else:
      sum = 0
      lastNeg = True
  return iMax, jMax

print(maxSubList([0,1,-1,3,-1,5]))