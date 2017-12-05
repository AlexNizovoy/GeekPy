# Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи
# повинні виконувати математичні операції з 2-ма числами, а саме додавання,
# віднімання, множення, ділення.
# Якщо під час створення екземпляру класу звернутися до атребута last_result
# він повинен повернути пусте значення
# Якщо використати один з методів - last_result повенен повернути результат
# виконання попереднього методу.
# Додати документування в клас

# Прикрутить к калькулятору текстовый документ с историей операций. Последние
# 10 операций (можно выбирать?). Последний результат тоже из файла
import json
import os

HISTORY_DIR = "results"
HISTORY_FILE = "history.dat"
HISTORY_FILE = HISTORY_DIR + os.sep + HISTORY_FILE


class Calc(object):
    """class Calc(object)
            Implement simple calculator with four base operations

            Init example:
                calc = Calc()
    """

    def __init__(self, history=10):
        """Constructor for Calc object.

        Object may be initiate with max count of items of history:
        obj = Calc(history=20) --> saves last 20 expressions
        obj = Calc(20) --> saves last 20 expressions
        obj = Calc() --> saves last 10 expressions (default)

        :param history: count of expressions to save in history file
        """
        self._hist_count = history
        if not os.path.isdir(HISTORY_DIR):
            os.mkdir(HISTORY_DIR)
        if os.path.isfile(HISTORY_FILE):
            self._hist = self.read_history(self._hist_count)
        else:
            self._hist = []
            with open(HISTORY_FILE, "w") as f:
                json.dump(self._hist, f)

    @staticmethod
    def read_history(hist_count=10):
        """Return N last expressions from history file

        :param hist_count: count of last expressions to return
        :return: list with dicts like {"expression": None, "result": None}
        """
        with open(HISTORY_FILE, "r") as f:
            result = json.load(f)
            try:
                result = result[-hist_count:]
            except TypeError:
                print("Error parsing history file! Invalid record format!")
                result = []
        return result

    def _history_update(self, a, b, result, action):
        expr = "{} {} {}".format(a, action, b)
        self._hist.append({"expression": expr, "result": result})
        # Check for count of history
        if len(self._hist) > self._hist_count:
            self._hist = self._hist[1:]
        with open(HISTORY_FILE, "w") as f:
            json.dump(self._hist, f)

    def view_history(self):
        self._hist = self.read_history(self._hist_count)
        print("---- Last {} expressions ----".format(self._hist_count))
        for i in self._hist:
            print("{expr} = {res}".format(expr=i.get("expression"),
                                          res=i.get("result")))
        print("---- END OF HISTORY ----")
        return self._hist

    @property
    def last_result(self):
        res = self.read_history(1)
        if not len(res):
            return None
        return res[0].get("result")

    def sum(self, a, b):
        """Return the result of the summation 'a' and 'b' and store it"""
        result = a + b
        self._history_update(a, b, result, "+")
        return result

    def sub(self, a, b):
        """Return the subtraction result 'a' from 'b' and store it"""
        result = a - b
        self._history_update(a, b, result, "-")
        return result

    def mul(self, a, b):
        """Return the result of multiplication 'a' to 'b' and store it"""
        result = a * b
        self._history_update(a, b, result, "*")
        return result

    def div(self, a, b):
        """Return the result of dividing 'a' to 'b' and store it.
            If 'b' == 0 - return None
        """
        if b:
            result = a / b
        else:
            result = None
        self._history_update(a, b, result, "/")
        return result

if __name__ == '__main__':
    calc = Calc(15)
    a, b = 15, 5
    print("{a} + {b} = {result}".format(a=a, b=b, result=calc.sum(a, b)))
    print("last_result = {result}".format(result=calc.last_result))
    print("{a} - {b}  {result}".format(a=a, b=b, result=calc.sub(a, b)))
    print("{a} * {b}  {result}".format(a=a, b=b, result=calc.mul(a, b)))
    print("last_result = {result}".format(result=calc.last_result))
    print("{a} / {b}  {result}".format(a=a, b=b, result=calc.div(a, b)))
    print("{a} / 0 = {result}".format(a=a, result=calc.div(a, 0)))
    print("last_result = {result}".format(result=calc.last_result))
    calc.view_history()
    new_calc = Calc(5)
    print("{a} / {b}  {result}".format(a=a, b=b, result=new_calc.div(a, b)))
    print("last_result = {result}".format(result=new_calc.last_result))
    new_calc.view_history()
    calc.view_history()
    # Створення нового екземпляру Calc() з меншим значенням 'history' зменшує
    # кількість історії в попередньо створеному екземплярі, оскільки вони
    # використовують один і той самий файл для збереження історії.
    # Можливий шлях побороти це - динамічно змінювати ім'я файлу історії
    # під час __init__() з додаванням до імені файлу номера екземпляра,
    # який зберігається в змінній класу.

    class New_calc(Calc):
        """Make some changes for multiply history files"""
        _counter = 0

        def __init__(self, history=20):
            New_calc._counter += 1
            self._hist_count = history

            self._history_file = HISTORY_FILE.split(".")
            self._history_file[-2] += str(New_calc._counter)
            self._history_file = ".".join(self._history_file)

            if not os.path.isdir(HISTORY_DIR):
                os.mkdir(HISTORY_DIR)
            if os.path.isfile(self._history_file):
                self._hist = self.read_history(self._hist_count)
            else:
                self._hist = []
                with open(self._history_file, "w") as f:
                    json.dump(self._hist, f)

        def read_history(self, hist_count=10):
            """Return N last expressions from history file

            :param hist_count: count of last expressions to return
            :return: list with dicts like {"expression": None, "result": None}
            """
            with open(self._history_file, "r") as f:
                result = json.load(f)
                try:
                    result = result[-hist_count:]
                except TypeError:
                    print("Error parsing history file! Invalid record format!")
                    result = []
            return result

        def _history_update(self, a, b, result, action):
            expr = "{} {} {}".format(a, action, b)
            self._hist.append({"expression": expr, "result": result})
            # Check for count of history
            if len(self._hist) > self._hist_count:
                self._hist = self._hist[1:]
            with open(self._history_file, "w") as f:
                json.dump(self._hist, f)

    calc = New_calc(15)
    a, b = 15, 5
    print("{a} + {b} = {result}".format(a=a, b=b, result=calc.sum(a, b)))
    print("last_result = {result}".format(result=calc.last_result))
    print("{a} - {b}  {result}".format(a=a, b=b, result=calc.sub(a, b)))
    print("{a} * {b}  {result}".format(a=a, b=b, result=calc.mul(a, b)))
    print("last_result = {result}".format(result=calc.last_result))
    print("{a} / {b}  {result}".format(a=a, b=b, result=calc.div(a, b)))
    print("{a} / 0 = {result}".format(a=a, result=calc.div(a, 0)))
    print("last_result = {result}".format(result=calc.last_result))
    calc.view_history()
    new_calc = New_calc(5)
    print("{a} / {b}  {result}".format(a=a, b=b, result=new_calc.div(a, b)))
    print("last_result = {result}".format(result=new_calc.last_result))
    new_calc.view_history()
    calc.view_history()
