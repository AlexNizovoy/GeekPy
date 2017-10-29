def season_1(month):
    """season_1(...)
            season_1(month)

            Return the season to whitch the entered month belongs
    """

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

            Return the season to whitch the entered month belongs
    """

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

            Return the season to whitch the entered month belongs
    """

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


def task_2_fn(numbers, base=None):
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
    # """2. Написати функцiю, яка буде приймати декiлька значень, одне з яких значення за замовченням(повинна бути перевiрка на наявнiсть), i у випадку якщо воно е додати його до iншого агрументу, якщо немае - придумайте логiку що робити программi."""

    print("\nНаписати функцiю, яка буде приймати декiлька значень, одне з яких значення за замовченням(повинна бути перевiрка на наявнiсть), i у випадку якщо воно е додати його до iншого агрументу, якщо немае - придумайте логiку що робити программi.")
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
    print("\n------Вивiд функцii------\n{}".format(task_2_fn(numbers, base)))


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
    # check for 'multiplicator' may be iterable or single number
    try:
        result = task_3_fn2(tpl, task_3_fn3, *multiplicator)
    except:
        result = task_3_fn2(tpl, task_3_fn3, multiplicator)
    return tuple(result)


def _task_3():
    # 3. Створiть 3 рiзних функцiї(на ваш вибiр), кожна з цих функцiй повинна повертати якийсь результат. Також створiть четверу ф-цiю, яка в тiлi викликае 3 попереднiб обробляе повернутий ними результат та також повертае результат. Таким чином ми будемо викликати 1 функцiю, а вона в своему тiлi ще 3
    print("3. Створено функцiю, яка за допомогою трьох iнших повертае кортеж, який складаеться з послiдовностi N елементiв, починаючи з позицii START з кроком STEP. Кожен з цих елементiв помножений на деяке число M")
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


def task_4_fn(x, y):
    """task_4_fn(x, y)

            Return tuple with result of comparasion 'x' and 'y'
            : x > y --> (1, x-y)
            : x < y --> (-1, y-x)
            : x == y --> (0, 0)
    """
    cmp = 0
    if x > y:
        cmp = 1
    elif x < y:
        cmp = -1
    return (cmp, abs(x - y))


def _task_4():
    #     4. •  Створiть 2 змiннi x та y з довiльними значеннями;
    # •  Створiть просту умовну конструкцiю(звiсно вона повинна бути в тiлi ф-цiї), пiд час виконання якої буде перевiрятися рiвнiсть змiнних x та y.
    # •  Удоскональте конструкцiю та додайте вiдповiднi умови, якi б при нерiвностi змiнних х та у вiдповiдь повертали рiзницю чисел.
    # •  Повиннi опрацювати такi умови:
    # •  x > y;       вiдповiдь - х бiльше нiж у на z
    # •  x < y;       вiдповiдь - у бiльше нiж х на z
    # •  x==y.     вiдповiдь - х дорiвнюе z
    print("\n4. Створено функцiю, що порiвнюе два числа та повертае результат порiвняння та рiзницю мiж числами.")
    try:
        x = float(input("Введiть перше число: "))
        y = float(input("Введiть друге число: "))
    except:
        print("Введено не число!")
        return None
    cmp, delta = task_4_fn(x, y)
    if cmp > 0:
        print("{0} бiльше нiж {1} на {2}".format(x, y, delta))
    elif cmp < 0:
        print("{1} бiльше нiж {0} на {2}".format(x, y, delta))
    else:
        print("{0} дорiвнюе {1}".format(x, y))


def task_5_fn(hash=None):
    """task_5_fn(hash=None)

            Return next result for string 'hash':
            : len(hash) < 30 --> 'print' sum of numbers in 'hash' and string with letters only
            : 30 <= len(hash) <= 50 --> 'print' len(), count of letters and numbers
            : 50 < len(hash) --> 'print' len(), count of letters and numbers and compare it.
                If count of numbers greater than count of letters - print sum of numbers;
                If counts are equal - alert count;
                If count of numbers less than count of letters - print division sum of numbers to count of letters
            : if count of numbers is 13 or 16 --> test this numbers for valid card number (Visa or MasterCard).
    """

    def count_num_ltr(s):
        """count_num_ltr(s)

            Parse string 's' and return tuple with 'count-of-numbers', 'count-of-letters' and 'sum-all-numbers'
        """
        num = 0
        ltr = 0
        num_sum = 0
        for i in s:
            if i.isnumeric():
                num += 1
                num_sum += int(i)
            elif i.isalpha():
                ltr += 1
        return num, ltr, num_sum

    def check_card(card):
        """check_card(card)

            Parse string 'card' and return tuple with (bool)'result-of-check' and (str)'name-of-card'
        """
        def check_Luhn(card):
            count = len(card)
            sum = 0
            # sum of odd right-to-left digits
            for i in card[(count-1)::-2]:
                sum += int(i)
            # sum of double even right-to-left digits
            for i in card[(count-2)::-2]:
                tmp = int(i) * 2
                if tmp >= 10:
                    tmp -= 9
                sum += tmp
            # check for last digit of sum is 0
            if sum % 10 == 0:
                return True

            return False

        passed = False
        if len(card) > 3 and card.isdigit():
            first_digits = int(card[:2])

            if len(card) == 13 or len(card) == 16:
                # Check for MasterCard
                if len(card) == 16 and 51 <= first_digits <= 55:
                    name = "MasterCard"
                    passed = check_Luhn(card)
                # Check for Visa
                elif 40 <= first_digits <= 49:
                    name = "Visa"
                    passed = check_Luhn(card)
        if not passed:
            name = "INVALID"

        return passed, name

    if not hash:
        print("Передано пустий рядок!")
        return None

    num, ltr, num_sum = count_num_ltr(hash)
    if len(hash) < 30:
        result = []
        for i in hash:
            if i.isalpha():
                result.append(i)
        print("Сума всiх чисел: {0}\nРешта букв: {1}".format(num_sum, "".join(result)))
    elif 30 <= len(hash) <= 50:
        print("Довжина рядка: {0}\nКiлькiсть букв: {1}\nКiлькiсть цифр: {2}".format(len(hash), ltr, num))
    else:
        if num > ltr:
            print("Сума всiх чисел: {0}".format(num_sum))
        elif num == ltr:
            print("Кiлькiсть букв та цифр однакова: {0}".format(num))
        else:
            print("Результат дiлення суми всих чисел на кiлькiсть лiтер: {0}".format(num_sum / ltr))

    if num in (13, 16):
        numbers = []
        for i in hash:
            if i.isnumeric():
                numbers.append(i)

        passed, name = check_card("".join(numbers))
        if passed:
            print("Цифри в рядку - номер валiдноi картки {}".format(name))
        else:
            print("Цифри в рядку не е номером валiдноi картки Visa або MasterCard")


def _task_5():
    #     5. •  маемо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" -> просто потицяв по клавi
    # •  створюете ф-цiю яка буде отримувати рядки на зразок мого, яка працюе в 4 випадках:
    # •  якщо довжина рядка в дфапазонi 30-50 -> прiнтуе довжину, кiлькiсть букв та цифр
    # •  якщо довжина менше 30 -> прiнтуе суму всiх чисел та окремо рядок без цифр лише з буквами
    # •  якщо довжина бульше 50 - > ваша фантазiя
    # •  звысно 4 все iнше
    print("\n5. Створено функцiю, що приймае на вхiд рядок та виконуе наступнi перевiрки:")
    print("   якщо довжина рядка менше 30 --> прiнтуе суму всiх чисел та окремо рядок без цифр лише з буквами;")
    print("   якщо довжина в дiапазонi [30, 50] --> прiнтуе довжину, кiлькiсть букв та цифр")
    print("   якщо довжина бiльше 50 --> прiнтуе довжину рядку, кiлькiсть лiтер та чисел та в залежностi вiд iх кiлькостi:")
    print("       якщо кiлькiсть чисел бiльша --> прiнтуе суму чисел;")
    print("       якщо кiлькiсть однакова --> прiнтуе цю кiлькiсть;")
    print("       якщо кiлькiсть чисел менша --> прiнтуе результат дiлення суми всих чисел на кiлькiсть лiтер.")
    print("   якщо кiлькiсть чисел 13 або 16 --> здiйснюеться перевiрка на належнiсть цих чисел до номера картки Visa або MasterCard.")

    hash = input("\nВведiть рядок для перевiрки: ")
    task_5_fn(hash)


def task_6_fn_1_factorial(num):
    """task_6_fn_1_factorial(num)

        Return a factorial of integer 'num'.
    """
    if num == 0:
        return 1
    num = abs(num)
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result


def task_6_fn_2_fibonacci(num):
    """task_6_fn_2_fibonacci(num)

        Return 'num' elements of Fibonacci's sequence.
    """
    num = abs(num)
    if num in (0, 1):
        return 0
    result = [0, 1]
    for i in range(2, num):
        result.append(result[i - 1] + result[i - 2])
    return result


def task_6_fn_3_simple(num):
    """task_6_fn_3_simple(num)

        Check if 'num' is simple. Return 'True' if it is.
    """
    num = abs(num)
    if num in (0, 1, 2):
        return True
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


def _task_6():
    # 6. придумайте 3 рiзних ф-цiї(немає рiзницi якi)
    print("6. Три функцii на вибiр:")
    print("   1. факторiал числа N")
    print("   2. вивiд послiдовностi з N чисел Фiбоначчi")
    print("   3. перевiрка цiлого числа на простоту (чи е воно простим)")
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
            1: task_6_fn_1_factorial,
            2: task_6_fn_2_fibonacci,
            3: task_6_fn_3_simple
        }.get(n, print)
        num = input("Введiть цiле число: ")
        if not len(num):
            return None
        try:
            num = int(num)
        except:
            print("Введено не цiле число!")
            continue
        print("\n------Вивiд функцii------\n{}".format(func(num)))


def task_7_fn_calculator(x=0, y=0, op=''):
    """task_7_fn_calculator(x=0, y=0, op='')

        It's a simple calculator.
        : 'x' and 'y' --> numbers (int or float)
        : 'op' --> operation with 'x' and 'y' (str in ('+', '-', '*', '/', '//', '**', '%'))
    """
    if op not in ("+", "-", "*", "/", "//", "**", "%"):
        return "Невiдома операцiя!"
    if y == 0 and op in ("/", "//", "%"):
        return "Дiлення на 0!"
    # return {
    #     '+': x + y,
    #     '-': x - y,
    #     '*': x * y,
    #     '/': x / y,
    #     '//': x // y,
    #     '**': x ** y,
    #     '%': x % y
    # }.get(op)
    # Wrong using - result computing anytime - if you put '1 * 0' - get ZeroDivisionError

    result = x
    if op == "+":
        result += y
    elif op == "-":
        result -= y
    elif op == "*":
        result *= y
    elif op == "**":
        result **= y
    elif op == "/":
        result /= y
    elif op == "//":
        result //= y
    else:
        result %= y
    return result


def _task_7():
    # 7. ну i традицiйно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи - один з яких операцiя яку зробити!
    def parse_number(s):
        try:
            s = int(s)
        except:
            try:
                s = float(s)
            except:
                s = 0
        return s

    print("\n7. Функцiя - простий калькулятор.")
    while True:
        x = parse_number(input("Введiть перше число: "))
        op = input("Введiть операцiю (пустий рядок для виходу): ").replace(" ", "")
        if not len(op):
            return None
        y = parse_number(input("Введiть друге число: "))

        print("{0} {2} {1} = {3}".format(x, y, op, task_7_fn_calculator(x, y, op)))


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
