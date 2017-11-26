# Напишіть програму в стилі ООП, що задовольняє наступним умовам: у програмі
# повинні бути два класи та два об'єкта, що належать різним класам; один
# об'єкт за допомогою методу свого класу повинен так чи інакше змінювати дані
# іншого об'єкта


class First(object):
    foo = []
    foo_sum = 0
    bar = 2

    def add_foo(self, number):
        self.foo.append(number)
        self.foo_sum += number

    def foo_mod_bar(self):
        return self.foo_sum % self.bar

    def view_args(self):
        args = ("foo", "foo_sum", "bar")
        for i in args:
            print("{} = {}".format(i, self.__getattribute__(i)))


class Second(object):
    def changer(self, obj, field, new_value):
        obj.__setattr__(field, new_value)


a = First()
b = Second()
a.add_foo(10)
a.add_foo(2)
a.add_foo(4)
a.view_args()
print("foo mod bar = ", a.foo_mod_bar())
print("-------------")
b.changer(a, "bar", 3)
a.view_args()
print("foo mod bar = ", a.foo_mod_bar())


# ----------------------- Second chance --------------
class Foo(object):
    foo = []
    foo_sum = 0
    bar = 2

    def add_foo(self, number):
        self.foo.append(number)
        self.foo_sum += number

    def foo_mod_bar(self):
        return self.foo_sum % self.bar

    def view_args(self):
        args = ("foo", "foo_sum", "bar")
        for i in args:
            print("{} = {}".format(i, self.__getattribute__(i)))


class Bar(Foo):
    def changer(self, new_value):
        Foo.bar = new_value


print("-----------------------------------------")
a = Foo()
b = Bar()
a.add_foo(10)
a.add_foo(2)
a.add_foo(4)
a.view_args()
print("foo mod bar = ", a.foo_mod_bar())
print("-------------")
b.changer(3)
a.view_args()
print("foo mod bar = ", a.foo_mod_bar())
