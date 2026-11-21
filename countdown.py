def countdown(n):
    while n >=1:
        yield n
        n -= 1
n=int(input("Enter a number: "))
for i in countdown(n):
    print(i)