# Створити клас Person, в якому буде присутнім метод __init__ який буде
# приймати * аргументів, які зберігатиме в відповідні змінні. Методи, які
# повинні бути в класі Person - show_age, print_name, show_all_information.
# Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
# атребут profession.


class Person(object):
    """class Person(object)
        Implement person object
    """
    def __init__(self, name, age, gender, **kwargs):
        """Constructor for Person object

        Keyword arguments:
        name --> (str) name of person
        age --> (int) age of person
        gender --> one of ("male", "female", "other", "not set")

        Other keyword arguments stored in self.args
        """
        self.name = name
        try:
            self.age = int(age)
        except ValueError:
            self.age = "error on set"
        if str(gender).lower() not in ("male", "female", "other", "not set"):
            self.gender = "not set"
        else:
            self.gender = gender.lower()
        self.args = kwargs

    def show_age(self):
        """Print and return age"""
        print("Age: {age}".format(age=self.age))
        return self.age

    def print_name(self):
        """Print and return name"""
        print("Name: {name}".format(age=self.name))
        return self.name

    def show_all_information(self):
        """Print and return tuple with tuples of arguments
        (only present in init)"""
        result = [
            ("name", self.name),
            ("age", self.age),
            ("gender", self.gender)
        ]
        for (k, v) in self.args.items():
            result.append((str(k), v))
        for i in result:
            print("{key}: {value}".format(key=i[0].capitalize(), value=i[1]))
        return tuple(result)

# -------------------Test------------------------------
person1 = Person("Alex", 33, "male", profession="crane operator")
person2 = Person("Jon", 25, "male")
person3 = Person("Mary", 31, "female")
person4 = Person("Anonymous", 40, "anon")
person5 = Person("Duncan M'cLaut", "immortal", "male", profession="highlander")
test = dict(person1.show_all_information())
