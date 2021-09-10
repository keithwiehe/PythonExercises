#Problem 1
def better_findA(arr):
    print(arr[better_findAHelper(arr, 0, len(arr)-1, -1)])

def better_findAHelper(arr, floor, cap, solution):
    print("time")
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


better_findA([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27, 28, 29, 30])
