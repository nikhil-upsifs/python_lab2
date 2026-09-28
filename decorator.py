def decorator(func):
   def wrapper():
       print("Function calling....")
       func()
       print("Function executed")
   return wrapper
@decorator
def greet():
   print("Hello, World!")
greet()