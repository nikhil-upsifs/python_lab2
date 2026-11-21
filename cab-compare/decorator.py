def decorator(add):
    def wrapper(a,b):
        print("Adding....")
        add(a,b)
        print("Thank you !!")
    return wrapper
@decorator 
def addition(a,b):
    print("Sum of given numbers :",a+b)
addition(4,5)