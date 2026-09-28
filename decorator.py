def decorator(func):
   def wrapper():
       print("Function calling....")
       func()
       print("Function executed")
   return wrapper
@decorator
def square():
    n=input("Enter a number: ")
    print("Square of the number is: ", int(n)**2)
square()