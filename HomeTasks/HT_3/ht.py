from random import randint, random
import time


def rnd_list(range_start=0, range_end=99, count=100000, base=1):
    """rnd_list(range_start=0, range_end=99, count=100000, base=1)
            Return list with "count" of rangom elements in range ["range_start", "range_end"].
            If "base" is integer or int - elements in list are integers, else - are floats.
    """
    result = []
    if isinstance(base, int) or type(base) == type(int):
        for i in range(count):
            result.append(randint(range_start, range_end))
    else:
        for i in range(count):
            result.append(random() * range_end + range_start)
    return result


def sort_selection(lst):
    """sort_selection(lst)
            Implementation of the algorithm selection sort.
            Return new sorted list.
    """
    result = lst[:]
    min_idx = 0
    for i in range(len(result)):
        min_el = result[i]
        is_min_found = False
        for k in range(i + 1, len(result)):
            if result[k] < min_el:
                min_el, min_idx = result[k], k
                is_min_found = True
        if is_min_found:
            result[i], result[min_idx] = result[min_idx], result[i]
    return result


def sort_insertion(lst):
    """sort_insertion(lst)
            Implementation of the algorithm insertion sort.
            Return new sorted list.
    """
    result = lst[:]
    for notsorted_idx in range(1, len(result)):
        if result[notsorted_idx] < result[notsorted_idx - 1]:
            tmp = result[notsorted_idx]
            idx = notsorted_idx - 1
            while tmp < result[idx] and idx >= 0:
                result[idx + 1] = result[idx]
                idx -= 1
            result[idx + 1] = tmp
    return result


def sort_bubble(lst):
    """sort_bubble(lst)
            Implementation of the algorithm bubble sort.
            Return new sorted list.
    """
    result = lst[:]
    length = len(result)
    for i in range(length):
        is_swapped = False
        for k in range(length - 1 - i):
            if result[k] > result[k + 1]:
                result[k], result[k + 1] = result[k + 1], result[k]
                is_swapped = True
        if not is_swapped:
            break
    return result


def main():
    COUNT = 10000
    print("HomeTask #3. Alexandr Nizovoy.\n")
    print("Generate random integers list... ", end="")
    list_int = rnd_list(count=COUNT, base=int)
    print("Done.\nGenerate random floats list... ", end="")
    list_float = rnd_list(count=COUNT, base=float)
    print("Done.\nBuilt-in sorting... ", end="")
    standart_int = list_int[:]
    standart_float = list_float[:]
    t0 = time.time()
    standart_int.sort()
    t1 = time.time()
    standart_float.sort()
    t2 = time.time()
    output = {}
    output["integers"] = {"Standart": (t1 - t0, True)}
    output["floats"] = {"Standart": (t2 - t1, True)}

    print("Done.\nBubble sorting... ", end="")
    t0 = time.time()
    res_int = sort_bubble(list_int)
    t1 = time.time()
    res_float = sort_bubble(list_float)
    t2 = time.time()
    output["integers"]["Bubble"] = (t1 - t0, res_int == standart_int)
    output["floats"]["Bubble"] = (t2 - t1, res_float == standart_float)

    print("Done.\nSelection sorting... ", end="")
    t0 = time.time()
    res_int = sort_selection(list_int)
    t1 = time.time()
    res_float = sort_selection(list_float)
    t2 = time.time()
    output["integers"]["Selection"] = (t1 - t0, res_int == standart_int)
    output["floats"]["Selection"] = (t2 - t1, res_float == standart_float)

    print("Done.\nInsertion sorting... ", end="")
    t0 = time.time()
    res_int = sort_insertion(list_int)
    t1 = time.time()
    res_float = sort_insertion(list_float)
    t2 = time.time()
    output["integers"]["Insertion"] = (t1 - t0, res_int == standart_int)
    output["floats"]["Insertion"] = (t2 - t1, res_float == standart_float)

    print("Done.\n-------------\n")
    print("For integers:")
    for name, result in output["integers"].items():
        print("{0} sort: time = {1[0]:.4}, the list is sorted correctly = {1[1]}".format(name, result))
    print("\n-------------\nFor floats:")
    for name, result in output["floats"].items():
        print("{0} sort: time = {1[0]:.4}, the list is sorted correctly = {1[1]}".format(name, result))


if __name__ == '__main__':
    main()
