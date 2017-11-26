# Створіть 3 класи, 2 з яких будуть успадковуватись один від одного!
# В суперкласі мається метод __init__ який приймає 2 атребути. Перегрузіть
# конструктор класу в дочірньому класі так, щоб додався ще один атребут.


class First(object):
    """docstring for First"""
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class Second(First):
    """docstring for Second"""
    def __init__(self, foo, bar, baz):
        First.__init__(self, foo, bar)
        self.baz = baz


class Third(Second):
    """docstring for Third"""
    def __init__(self, foo, bar, baz, spam):
        Second.__init__(self, foo, bar, baz)
        self.spam = spam


a = First(1, 2)
b = Second(3, 4, 5)
c = Third(6, 7, 8, 9)


def print_args(obj):
    """Extract end print arguments from object"""
    tmp = dir(obj)
    f = list(filter(lambda x: x[0] != "_", tmp))
    for i in f:
        print("{key}: {value}".format(key=i, value=obj.__getattribute__(i)))


print("--- a ---")
print_args(a)
print("--- b ---")
print_args(b)
print("--- c ---")
print_args(c)
