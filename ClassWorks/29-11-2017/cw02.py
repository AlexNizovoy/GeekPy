class Worker(object):

    @staticmethod
    def celery(tax, celery=None):
        if celery:
            return tax + 5
        else:
            return tax


if __name__ == '__main__':
    vasya = Worker()
    print(vasya.celery(5, 5))
