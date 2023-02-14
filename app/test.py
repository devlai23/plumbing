dbNum = '((561,),)'
count = ""; 
for i in dbNum:
    print("hi", i)
    if i.isdigit():
        count += i
print(count)