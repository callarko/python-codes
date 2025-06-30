x=int(input("Enter First Number :"))
y=int(input("Enter Second Number :"))
z=int(input("Enter Third Number :"))
min=mid=max=None
if((x<y) & (x<z)):
    if(y<z):
        min,mid,max=x,y,z
    else:
        min,mid,max=x,z,y
elif ((y<z) & (y<x)):
    if(x<z):
        min,mid,max=y,x,z
    else:
        min,mid,max=y,z,x
else:
    if(x<y):
        min,mid,max=z,x,y
    else:
        min,mid,max=z,y,x
print("The Numbers in ascending order : ", min,mid,max)