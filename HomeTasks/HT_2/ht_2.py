# 1. (таких ф-цiй потрiбно написати 3 -> рiзними варiантами) Написати функцiю season, приймаючу 1 аргумент — номер мiсяця (вiд 1 до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь).
def season_1(month):
    """season_1(...)
            season_1(month)

            Return the season to whitch the entered month belongs"""

    season = (month % 12) // 3
    return {
        0: "зима",
        1: "весна",
        2: "лiто",
        3: "осiнь",
    }.get(season, "Щось не так :(")


def season_2(month):
    """season_2(...)
            season_2(month)

            Return the season to whitch the entered month belongs"""

    if month in (12, 1, 2):
        return "зима"
    elif month in (3, 4, 5):
        return "весна"
    elif month in (6, 7, 8):
        return "лiто"
    elif month in (9, 10, 11):
        return "осiнь"
    else:
        return "Невiдомий мiсяць"


def season_3(month):
    """season_3(...)
            season_3(month)

            Return the season to whitch the entered month belongs"""

    if 1 <= month <= 2 or month == 12:
        return "зима"
    elif 3 <= month <= 5:
        return "весна"
    elif 6 <= month <= 8:
        return "лiто"
    elif 9 <= month <= 11:
        return "осiнь"
    else:
        return "Невiдомий мiсяць"


def _task_1():
    # """1. (таких ф-цiй потрiбно написати 3 -> рiзними варiантами) Написати функцiю season, приймаючу 1 аргумент — номер мiсяця (вiд 1 до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)."""

    print("\nНаписати функцiю season, приймаючу 1 аргумент - номер мiсяця (вiд 1 до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь).")
    print("(таких ф-цiй потрiбно написати 3 -> рiзними варiантами)")
    while True:
        n = input("Введiть номер функцiї (пустий рядок для повернення в головне меню): ")
        if not len(n):
            return None
        try:
            n = int(n)
        except:
            print("Невiрне значення номеру завдання!")
            continue
        func = {
            1: season_1,
            2: season_2,
            3: season_3
        }.get(n, print)
        month = input("Введiть номер мiсяця: ")
        if not len(month):
            return None
        try:
            month = int(month)
        except:
            print("Невiрне значення мiсяця!")
            continue
        print("Мiсяць №{} - це {}.\n".format(month, func(month)))


def func_task_2(numbers, base=None):
    """func_task_2(numbers, base=None)

            Compute the sum of integers in iterable 'numbers' and return result in 'base' number system. If 'base' not specefied - use decimal
            """

    def dec(n):
        return n

    if not base:
        base = 10

    result = 0
    for i in numbers:
        result += i

    f = {
        2: bin,
        8: oct,
        10: dec,
        16: hex
    }.get(base, dec)

    return f(result)


def _task_2():
    # """2. Написати функцiю, яка буде приймати декiлька значень, одне з яких значення за замовченням(повинна бути перевiрка на наявнiсть), i у випадку якщо воно є додати його до iншого агрументу, якщо немає - придумайте логiку що робити программi."""

    print("\nНаписати функцiю, яка буде приймати декiлька значень, одне з яких значення за замовченням(повинна бути перевiрка на наявнiсть), i у випадку якщо воно є додати його до iншого агрументу, якщо немає - придумайте логiку що робити программi.")
    print("\nФункцiя, що сумуе введенi агрументи (цiлi числа), а при наявностi iменованого аргумента 'base', що е основою счислення, виводить результат у вибранiй системi (2, 8, 10, 16)")
    numbers = input("\nВведiть групу цiлих чисел (через пробiл): ").split()
    # convert space-separated string into list
    for i in range(len(numbers)):
        try:
            numbers[i] = int(numbers[i])
        except:
            numbers[i] = 0

    try:
        base = int(input("Введiть цiле число: "))
    except:
        base = None
    print("\n------Вивiд функцii------\n{}".format(func_task_2(numbers, base)))


def _task_3():
    pass


def _task_4():
    pass


def _task_5():
    pass


def _task_6():
    pass


def _task_7():
    pass


if __name__ == '__main__':
    print("HomeTask #2. Alex Nizovoy.\n")
    while True:
        n = input("Введiть номер завдання (пустий рядок для виходу): ")
        if not len(n):
            print("На все добре!")
            exit(0)
        try:
            n = int(n)
        except:
            print("Невiрне значення номеру завдання!")
            continue
        task = {
            1: _task_1,
            2: _task_2,
            3: _task_3,
            4: _task_4,
            5: _task_5,
            6: _task_6,
            7: _task_7
        }.get(n, print)
        task()
