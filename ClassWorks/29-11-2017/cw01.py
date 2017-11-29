class A(object):
    tax = 5

    @staticmethod
    def celery():
        return A.tax + 5


if __name__ == '__main__':
    a = A()
    print(a.celery())
