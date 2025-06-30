num1=int(input("Enter First Number : "))
num2=int(input("Enter Second Number : "))
if(num2<num1):
    t= num2*num1
    t= t+10
    print(num1,num2,t)
elif(num2>num1) :
    t=num2*num1
    t=t+100
    print(num1,num2,t)
else :
    print("num1 and num2 are equeal")