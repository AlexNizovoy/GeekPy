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


def task_1():
    """1. (таких ф-цiй потрiбно написати 3 -> рiзними варiантами) Написати функцiю season, приймаючу 1 аргумент — номер мiсяця (вiд 1 до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)."""

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


def task_2():
    pass


def task_3():
    pass


def task_4():
    pass


def task_5():
    pass


def task_6():
    pass


def task_7():
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
            1: task_1,
            2: task_2,
            3: task_3,
            4: task_4,
            5: task_5,
            6: task_6,
            7: task_7
        }.get(n, print)
        task()
