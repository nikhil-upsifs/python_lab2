def Double_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper
@Double_result
def add(a, b):
    return a + b   
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
print("Double the sum is: ", add(a, b))
