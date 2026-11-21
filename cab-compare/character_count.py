
s=input("Enter a string : ")
def character_count(s):
    count=0
    for i in s:
        count+=1
    return count
print("Number of characters in the string :",character_count(s))