amount = float(input("Enter the MRP : "))
if amount <= 1000:
    print("You get 10% discount i.e. : ", amount - 10/100)
elif amount > 1000 and amount <= 5000:
    print("You get 20% discount i.e. : ", amount - 20/100)
elif amount > 5000 and amount <= 10000:
    print("You get 30% discount i.e. : ", amount - 30/100)
elif amount > 10000:
    print("You get 50% discount i.e. :", amount - 50/100)
    