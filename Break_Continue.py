a=b=c=0
for i in range(1,11):
    a=int(input("Enter number 1 : " ))
    b=int(input("Enter number 2 : " ))
    if b==0:
        print("Division by zero hits infinite loop! Aborting")
        break
    else:
        c=a/b
        print (c)
        print ("program over")