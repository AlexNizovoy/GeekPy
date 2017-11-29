class A(object):
    counter = 0

    def __init__(self):
        A.counter += 1
        print("Count: {}".format(A.counter))

    def __del__(self):
        A.counter -= 1
        print("Count: {}".format(A.counter))

    def count(self):
        print(A.counter)


if __name__ == '__main__':
    a = A()
    b = A()
    c = A()
    del a
    del b
    del c
