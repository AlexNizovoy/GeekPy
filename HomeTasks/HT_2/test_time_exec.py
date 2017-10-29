import time


def w_str(s):
    result = ""
    for i in s:
        result += i
    return result


def w_arr(s):
    result = []
    for i in s:
        result.append(i)
    return "".join(result)


def w_arr2(s):
    result = []
    for i in s:
        result.append(i)
    return str(result)


def test():
    print("Start test...")
    tst = "".join([str(n) for n in range(1000)])
    t0 = time.time()
    for i in range(10000):
        w_str(tst)
    t1 = time.time()
    for i in range(10000):
        w_arr(tst)
    t2 = time.time()
    for i in range(10000):
        w_arr2(tst)
    t3 = time.time()

    print("End test.")
    print("time for w_str: {}".format(t1 - t0))
    print("time for w_arr: {}".format(t2 - t1))
    print("time for w_arr2: {}".format(t3 - t2))

# >>> import test_time_exec
# >>> test_time_exec.test()
# Start test...
# End test.
# time for w_str: 7.609375
# time for w_arr: 6.46875
# time for w_arr2: 11.25
# >>> test_time_exec.test()
# Start test...
# End test.
# time for w_str: 7.484375
# time for w_arr: 6.5625
# time for w_arr2: 11.234375
# >>>
#
# Висновок - для перебору та обробки символів рядка з наступним створенням нового швидше використовувати роботу з list аніж зі string


def test2(n=10000):
    print("Start test...")
    tst = "".join([str(n) for n in range(1000)])
    ll = 1000
    t0 = time.time()
    for i in range(n):
        len(tst) > 0
    t1 = time.time()
    for i in range(n):
        ll > 0
    t2 = time.time()

    print("End test.")
    print("time for get len(): {}".format(t1 - t0))
    print("time for compare int: {}".format(t2 - t1))

# >>> test_time_exec.test2(100000)
# Start test...
# End test.
# time for get len(): 0.03125
# time for compare int: 0.015625
# >>> test_time_exec.test2(10000)
# Start test...
# End test.
# time for get len(): 0.015625
# time for compare int: 0.0
# >>> test_time_exec.test2(10000000)
# Start test...
# End test.
# time for get len(): 2.625
# time for compare int: 1.40625
# >>>
#
# Висновок - порівняння визначення довжини рядку займає більше часу, ніж порівняння з попередньо взятим значенням, але різниця помітна тільки при надвеликих значеннях.
