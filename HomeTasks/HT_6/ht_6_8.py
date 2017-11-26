# Створіть клас, який називається DefaultClass що має атрибути об'єкту name,
# symbol number . Виведіть атребути.
# Створіть словник з наступними ключами і значеннями: 'name': 'Vasya',
# 'l_name': 'Pupkin', 'age': 20 . Далі створіть об'єкт з ім'ям user класу
# DefaultClass1за допомогою цього словника.
# Для класу DefaultClass1 визначте метод з ім'ям print_info() , що виводить на
# екран значення атрибутів об'єкта (name , l_name та age ).


class DefaultClass(object):
    name = "John"
    symbol = "D"
    number = "42"

for i in ("name", "symbol", "number"):
    print("{i} = {v}".format(i=i, v=DefaultClass().__getattribute__(i)))

dct = {"name": "Vasya", "l_name": "Pupkin", "age": 20}


class DefaultClass1(object):
    def __init__(self, name, l_name, age):
        self.name = name
        self.l_name = l_name
        self.age = age

    def print_info(self):
        for i in ("name", "l_name", "age"):
            print("{i}: {v}".format(i=i, v=self.__getattribute__(i)))

user = DefaultClass1(**dct)
user.print_info()
