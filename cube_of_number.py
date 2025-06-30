def cube(number):
  return number * number * number

def thrice(number):
  return number * 3

number = int(input("Enter a number: "))

cube_value = cube(number)
thrice_value = thrice(number)

print("The cube of the number is", cube_value)
print("The thrice value of the number is", thrice_value)