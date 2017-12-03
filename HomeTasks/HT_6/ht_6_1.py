# Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи
# повинні виконувати математичні операції з 2-ма числами, а саме додавання,
# віднімання, множення, ділення.
# Якщо під час створення екземпляру класу звернутися до атребута last_result
# він повинен повернути пусте значення
# Якщо використати один з методів - last_result повенен повернути результат
# виконання попереднього методу.
# Додати документування в клас


class Calc(object):
    """class Calc(object)
        Implement simple calculator with four base operations

        Init example:
            calc = Calc()

        Attributes:
            last_result: store result of last operation.
                Initial value - None
    """
    def __init__(self):
        """Constructor for Calc object."""
        self.last_result = None

    def sum(self, a, b):
        """Return the result of the summation 'a' and 'b' and store it"""
        self.last_result = a + b
        return self.last_result

    def sub(self, a, b):
        """Return the subtraction result 'a' from 'b' and store it"""
        self.last_result = a - b
        return self.last_result

    def mul(self, a, b):
        """Return the result of multiplication 'a' to 'b' and store it"""
        self.last_result = a * b
        return self.last_result

    def div(self, a, b):
        """Return the result of dividing 'a' to 'b' and store it.
            If 'b' == 0 - return None
        """
        if b:
            self.last_result = a / b
            return self.last_result
        else:
            self.last_result = None
            return None
# -------------------Test------------------------------
calc = Calc()
a, b = 15, 5
print("{a} + {b} = {result}".format(a=a, b=b, result=calc.sum(a, b)))
print("last_result = {result}".format(result=calc.last_result))
print("{a} - {b}  {result}".format(a=a, b=b, result=calc.sub(a, b)))
print("{a} * {b}  {result}".format(a=a, b=b, result=calc.mul(a, b)))
print("last_result = {result}".format(result=calc.last_result))
print("{a} / {b}  {result}".format(a=a, b=b, result=calc.div(a, b)))
print("{a} / 0 = {result}".format(a=a, result=calc.div(a, 0)))
print("last_result = {result}".format(result=calc.last_result))
