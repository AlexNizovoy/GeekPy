# Створіть клас в якому буде атребут який буде рахувати кількість створених
# екземплярів класів.


class Foo(object):
    counter = 0

    def __init__(self):
        self.__class__.counter += 1
        print(self.counter)

    def __del__(self):
        self.__class__.counter -= 1
        print(self.counter)

    def view_count(self):
        print(self.counter)

a = Foo()
b = Foo()
c = Foo()
d = c
a.view_count()
b.view_count()
c.view_count()
d.view_count()
del a
del b
del c
print("del d")
del d
# Метод __del__() викликається після того, як знищена останнє посилання на
# створений об'єкт. Оскільки посилання на об'єкт 'с' зберігалось в змінній
# 'd', то метод __del__() не викликався при виконанні команди 'del c', а
# тільки після 'del d'
