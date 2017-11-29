class Worker(object):
    _tax = 5

    @property
    def celery(self):
        return self._tax + 5


if __name__ == '__main__':
    vasya = Worker()
    print(vasya.celery)
