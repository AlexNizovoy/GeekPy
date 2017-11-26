# Створити пустий клас, який називається Thing. Потім створіть об'єкт example
# цього класу. Виведіть типи зазначених об'єктів.
# Створіть новий клас Thing2 і призначте йому атрибут letters зі значенням
# 'abc' . Виведіть на екран значення атрибута letters.
# Створіть ще один клас Thing3 . Присвойте значення 'xyz' атрибуту об'єкта,
# який називається letters. Виведіть на екран значення атрибута letters .


class Thing(object):
    pass


example = Thing()
print(type(Thing()))
print(type(example))
print("----------------")


class Thing2(object):
    letters = "abc"


print("Thing2.letters = ", Thing2().letters)


class Thing3(object):
    letters = "xyz"


print("Thing3.letters = ", Thing3().letters)
