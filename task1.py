class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Division by zero is not allowed."

    def calculate(self, a, b, operator):
        if operator == '+':
            return self.add(a, b)
        elif operator == '-':
            return self.subtract(a, b)
        elif operator == '*':
            return self.multiply(a, b)
        elif operator == '/':
            return self.divide(a, b)
        else:
            return "Invalid operator"

def main():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    operator = input("Enter operator (+, -, *, /): ")

    calculator = Calculator()
    result = calculator.calculate(a, b, operator)
    print("Result:", result)

if __name__ == "__main__":
    main()
