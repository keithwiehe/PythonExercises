def exercise1(num1, num2):
    #started inputted the number through function call so they
    #would all complete when file was run
    #num1 = int(input("Enter first number:"))
    #num2 = int(input("Enter second number:"))
    print("First number ", num1, "\n Second number ", num2, "Solution: ")
    product = num1 * num2
    if(product > 1000):
        print(num1+num2)
    else:
        print(product)

def exercise2():
    previous = 0
    for i in range(10):
        print("Current number ", i, " Previous number ", previous,
        "Sum: ", previous + i)
        previous = i

def exercise3(input):
    for i in range(0, len(input) - 1, 2):
        print(input[i])

def exercise4(input, amount):
    if amount > len(input):
        print("Error, More characters are asked to be deleted than the string has.")
    else:
        word =""
        for i in range(amount, len(input)):
            word = word + input[i]
        print(word)

def exercise5(arr):
    print("Given list: ", arr)
    if(arr[0] == arr[len(arr)-1]):
        print("True")
    else:
        print("False")

def exercise6(arr):
    print("Given list: ", arr)
    print("Numbers divisible by 5:")
    isEmpty = True
    for i in range(len(arr)):
        if arr[i] % 5 == 0:
            isEmpty = False
            print(arr[i])
    if isEmpty:
        print("No numbers in the list were divisible by 5")

def exercise7(input):
    find = "Emma"
    print(find, " was found ", input.count(find), "times in the given string.")

def exercise8(num):
    for i in range(num+1):
        for k in range(i):
            print(i, end=" ")
        #Empty so that it prints a singular new line. If '\n' added it prints two
        print()

def exercise9(num):
    print("Original number is: ", num)
    revNum = 0
    numcopy = num
    while(num > 0):
        mod = num % 10
        #/ gave decimals and weird things happened. Including while statement
        #being ignored. // is floor division which stops at round numbers and zero
        num = num // 10
        revNum = (revNum * 10) + mod
        # print("revNum: ", revNum, "num: ", num)
    if revNum == numcopy:
        print("The original number and the reverse number the same")
    else:
        print("The original number and the reverse number are not the same")

def exercise10(arr1, arr2):
    print("list1 = ", arr1)
    print("list2 = ", arr2)
    combinedArr = []
    #found for loop will auto iterate through array in Python
    #Left older exercises as is
    for numOdd in arr1:
        if numOdd % 2 != 0:
            combinedArr.append(numOdd)
    for numEven in arr2:
        if numEven % 2 == 0:
            combinedArr.append(numEven)
    print("result list is ", combinedArr)

def exercise11(num):
    #copied several lines from exercise9 
    print("Original number is: ", num)
    arr = []
    while(num > 0):
        mod = num % 10
        #/ gave decimals and weird things happened. Including while statement
        #being ignored. // is floor division which stops at round numbers and zero
        num = num // 10
        arr.append(mod)
    for num in arr:
        print(num, end=" ")
    print()
    
def exercise12(num):
    tax = 0
    #highest tax bracket
    if(num > 20000):
        tax = (num - 20000) * 0.2
        tax += 1000
    elif num > 10000:
        tax = (num - 10000) * 0.1
    print("The taxed amount on $", num, "is $", tax)

def exercise13(num):
    for i in range(1, num + 1):
        for k in range(1, num +1):
            product = i * k
            print(product, end=" ")
        print()

def exercise14(input, num):
    for i in range(num, 0, -1):
        for k in range(i):
            print(input, end=" ")
        print()

#wanted to stick with the exercisenumber theme
def exercise15(base, power):
    exponent(base, power)

def exponent(base, exp):
    if exp < 0:
        print("Error, exponent given is less than 0")
    if exp == 0:
        num = 1
    else:
        num = base
        for i in range(1, exp):
            num = num * base
    print("base = ", base)
    print ("exponent = ", exp)
    if exp > 1:
        print(base, "raised to the power of ", exp, "is: ", num, "i.e. (", end='')
        for i in range(exp):
            print(base, '*', end=" ")
        print(" = ", num, ")")
    else:
        print(base, "raised to the power of ", exp, "is: ", num)

#exectution of all exercises        
print("Exercise 1")
exercise1(10, 20)
exercise1(100, 20)
print("Exercise 2")
exercise2()
print("Exercise 3")
exercise3("pynative")
print("Exercise 4")
#exercise4("pynative", 14)
exercise4("pynative", 4)
print("Exercise 5")
#exercise5([1,6,7,8,9,12,13])
exercise5([1,56,17,8,9,12,1])
print("Exercise 6")
exercise6([1,60,75,8,90,125,13])
#exercise6([1,56,17,8,9,12,1])
print("Exercise 7")
exercise7("Emma is good developer. Emma is a writer")
print("Exercise 8")
exercise8(5)
print("Exercise 9")
exercise9(121)
exercise9(1222)
print("Exercise 10")
exercise10([10, 12, 13, 14, 17], [9, 7, 10, 14, 19])
print("Exercise 11")
exercise11(789)
print("Exercise 12")
exercise12(78000)
print("Exercise 13")
exercise13(10)
print("Exercise 14")
exercise14('*', 5)
print("Exercise 15")
exercise15(2, 5)
exercise15(2, 1)
exercise15(2, 0)
