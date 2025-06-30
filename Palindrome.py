n = int(input("Enter a number : "))
m = n
reverse = 0
while  n > 0:
    r = n % 10
    n = n // 10
    reverse = reverse * 10 + r

if m == reverse:
    print("The number is palindrome : ")
else:
    print("The number is not palindrome")
    