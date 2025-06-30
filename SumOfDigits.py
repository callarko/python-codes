n = int(input("Enter a number : "))
sum = 0
while  n > 0:
    r = n % 10
    n = n // 10
    
    sum = sum + r
    
print("Sum of the digits is : ", sum)