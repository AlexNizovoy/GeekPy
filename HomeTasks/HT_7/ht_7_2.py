# Придумать два класса: один с двумя статическими методами, второй -
# с Проперти. Потом пример вызова.


# --------------- Сорри, неведомый поток кода. Создал, а убивать жалко :( ---
# ---------------- START ----------------
# class A(object):
#     """Some class"""
#     def __init__(self, *args):
#         self.args = list(args)

#     def mapper(self, fnc, *args):
#         for i in range(len(self.args)):
#             self.args[i] = fnc(self.args[i], *args)


# if __name__ == '__main__':
#     tst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     a = A(*tst)

#     def multiply(a, b):
#         return a * b

#     print(a.args)
#     a.mapper(multiply, 2)
#     print(a.args)
# ------------------ END -----------------

class Data(object):
    """Data object"""
    def __init__(self, day, month, year, sep="."):
        self.day = day
        self.month = month
        self.year = year
        self.separator = sep

    def __str__(self):
        return "{d}{sep}{m}{sep}{y}".format(d=self.day, m=self.month,
                                            y=self.year, sep=self.separator)

    @staticmethod
    def validate(obj):
        """Simple and stupid validation of date"""
        if 0 < obj.day <= 31 and 0 < obj.month <= 12 and 0 < obj.year < 4000:
            return True
        else:
            return False

    @staticmethod
    def is_leap_year(year):
        if ((year % 4 == 0 and year % 100 != 0) or
                (year % 400 == 0)):
            return True
        else:
            return False


class A(object):
    """Some class"""
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self._c = 100

    @property
    def hidden_sum(self):
        return self.a + self.b + self._c

    @property
    def hidden_crazy_op(self):
        return self.hidden_sum * self.a * self.b / self._c


if __name__ == '__main__':
    a = Data(4, 12, 2017)
    b = Data(31, 31, 2017)
    print(Data.validate(a))
    print(Data.validate(b))
    print(Data.is_leap_year(2017))
    print(Data.is_leap_year(2000))
    print("-------------------")
    c = A(2, 5)
    print(c.hidden_sum)
    print(c.hidden_crazy_op)
