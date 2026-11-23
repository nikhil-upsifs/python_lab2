class calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    def add(self):
        return self.num1 + self.num2
    def subtract(self):
        if self.num1 < self.num2:
            return self.num2 - self.num1
        else:
            return self.num1 - self.num2
    def multiply(self):
        return self.num1 * self.num2
    def divide(self):
        if self.num2 == 0:
            return "Error: Division by zero"
        else:
            return self.num1 / self.num2
Calc1=calculator(10, 5)
print("Addition:", Calc1.add())
print("Subtraction:", Calc1.subtract())
print("Multiplication:", Calc1.multiply())
print("Division:", Calc1.divide())