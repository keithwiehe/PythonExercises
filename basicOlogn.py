#given is O(n)
def findA(L):
    for i in range(len(L)):
        left = i-1
        right = i+1
        if i == 0:
            left = i
        if i == len(L)-1:
            right = i
        if L[left] <= L[i] >= L[right]:
            return L[i]
#My O log(n)

#not quite need to resplit if L > 3 or so
def findLogA(L):
    j = len(L-1)
    for i in range(len(L)):
        #psuedocode assuming no errors and one exists
        if j == i:
            return L[j]
        #check from beginning
        ileft = i-1
        iright = i+1
        if i == 0:
            ileft = i
        if i == len(L)-1:
            iright = i
        if L[ileft] <= L[i] >= L[iright]:
            return L[i]
        #check from end
        jleft = i-1
        jright = i+1
        if j == 0:
            jleft = i
        if j == len(L)-1:
            jright = i
        if L[jleft] <= L[i] >= L[jright]:
            return L[i]
        j -= j

def better_findA(arr):
    print(arr[better_findAHelper(arr, 0, len(arr)-1, -1)])

def better_findAHelper(arr, floor, cap, solution):
    print("TIME")
    canLeft = True
    canRight = True
    pivot = floor + ((cap - floor) // 2)
    left = pivot - 1
    right = pivot + 1
    if(pivot == floor):
        canLeft = False
    if(pivot == cap):
        canRight = False
    if(pivot == 0):
        left = pivot
    if pivot == len(arr) - 1:
        right = pivot
    if arr[left] <= arr[pivot] >= arr[right]:
        print("Solution: ", pivot, "From: ",arr[left], " <= ",arr[pivot], " >= ",arr[right])
        return pivot
    else:
        if arr[left] >= arr[pivot] and canLeft:
            # print("First IF")
            solution = better_findAHelper(arr, floor, left, solution)
        elif canLeft:
            # print("Second IF")
            if left == floor:
                left = floor + 1
            solution = better_findAHelper(arr, floor, left - 1, solution)
        if solution > -1:
            return solution
        if arr[right] >= arr[pivot] and canRight:
            # print("Third IF")
            solution = better_findAHelper(arr, right,cap, solution)
        elif canRight:
            # print("Fourth IF")
            if right == cap:
                right = cap - 1
            solution = better_findAHelper(arr, right + 1, cap, solution)
    return solution

better_findA([1,2,3,4,5,6,7,8,9,10])