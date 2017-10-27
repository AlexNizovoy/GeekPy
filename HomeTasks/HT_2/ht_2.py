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


def task_3_fn1(start, count, step=1):
    """task_3_fn1(start, count, step=1)

            Return a tuple with 'count' elements starts from 'start' with 'step' increment/decrement
            """
    try:
        step = int(step)
    except:
        step = 1

    if step == 0:
        step = 1

    i = count * step + start
    return tuple(range(start, i, step))


def task_3_fn2(iterable, map_fnc=None, *args):
    """task_3_fn2(iterable, map_fnc)

            Return a list with elements from 'iterable' treated by function 'map_fnc' ('map_fnc(iterable[n])')
            If 'map_fnc' is None or not-a-function - return 'iterable'
            """
    if not map_fnc or not callable(map_fnc):
        return iterable

    result = []
    for i in iterable:
        result.append(map_fnc(i, *args))

    return result


def task_3_fn3(x, *args):
    """task_3_fn3(x, *args)

            Return a result of multiplication 'x' to each elements in 'args'
            """
    result = x
    for i in args:
        result *= i
    return result


def task_3_fn4(start, count, step, multiplicator):
    """task_3_fn4(start, count, step, multiplicator)

            Return tuple of 'count' elements from 'start' with 'step' increment multiply by 'multiplicator'
            'multiplicator' may be iterable
            """
    tpl = task_3_fn1(start, count, step)
    try:
        result = task_3_fn2(tpl, task_3_fn3, *multiplicator)
    except:
        result = task_3_fn2(tpl, task_3_fn3, multiplicator)
    return tuple(result)


def _task_3():
    # 3. Створiть 3 рiзних функцiї(на ваш вибiр), кожна з цих функцiй повинна повертати якийсь результат. Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднiб обробляє повернутий ними результат та також повертає результат. Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3
    print("3. Створено функцiю, яка за допомогою трьох iнших повертає кортеж, який складається з послiдовностi N елементiв, починаючи з позицii START з кроком STEP. Кожен з цих елементiв помножений на деяке число M")
    start = input("\nВведiть цiле число START: ")
    count = input("Введiть кiлькiсть елементiв послiдовностi: ")
    step = input("Введiть крок STEP (залиште пустим для кроку 1): ")
    multiplicator = input("Введiть число M (залиште пустим для значення 1): ")
    try:
        start = int(start)
        count = int(count)
        if step:
            step = int(step)
        else:
            step = 1
        if multiplicator:
            multiplicator = int(multiplicator)
        else:
            multiplicator = 1
    except:
        print("Введено неправильне значення!")
        return None

    result = task_3_fn4(start, count, step, multiplicator)
    print("\n------Вивiд функцii------\n{}".format(result))


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
