def even_numbers(n):
    for i in range(0,n+1, 2):
        yield i

n=int(input("Enter a number: "))
for i in even_numbers(n):
    print(i,end=" ")