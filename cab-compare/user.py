user = input ("Enter Email:")
i=0
user2=""
while(user[i]!='@'):
    user2+=user[i]
    i+=1
print("user ID from given email:",user2)
