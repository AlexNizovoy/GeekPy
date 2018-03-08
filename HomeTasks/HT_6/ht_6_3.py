# Напишіть програму, де клас «геометричні фігури» (figure) містить
# властивість color з початковим значенням white і метод для зміни кольору
# фігури, а його підкласи «овал» (oval) і «квадрат» (square) містять методи
# __init__ для завдання початкових розмірів об"єктів при їх створенні.
# Видозмініть програму так, щоб метод __init__ мався в класі «геометричні
# фігури» та приймав кольор фігури при створенні екземпляру, а методи
# __init__ підкласів доповнювали його та додавали початкові розміри.


class Figure(object):
    """class Figure()

    Create geometric figure object.
    Attributes:
        color --> default value = "white"
    """
    color = "white"
    palette = ("white", "silver", "gray", "black", "red", "maroon",
               "yellow", "olive", "lime", "green", "aqua", "teal", "blue",
               "navy", "fuchsia", "purple")

    def set_color(self, color):
        """set_color(color)

        Method of Figure object.
        Setting up attribute "color" of object.
        "color" must be in the list contained in the attribute .palette
        If "color" not in list - raise ValueError
        """
        if str(color).lower() not in self.palette:
            raise ValueError("'{}' is incorrect color! \
To get list of colors use: .palette".format(color))
        else:
            self.color = color.lower()


class Oval(Figure):
    """class Oval(Figure)

    Create object oval - geometric figure
    """
    def __init__(self, height, width):
        """Constructor for Oval object

        Keyword arguments:
        height --> (int)
        width --> (int)
        """
        self.height = height
        self.width = width


class Square(Figure):
    """class Square(Figure)

    Create object square - geometric figure
    """
    def __init__(self, height, width):
        """Constructor for Square object

        Keyword arguments:
        height --> (int)
        width --> (int)
        """
        self.height = height
        self.width = width


class Figure_new(object):
    """class Figure()

    Create geometric figure object.
    Attributes:
        color --> default value = "white"
    """
    palette = ("white", "silver", "gray", "black", "red", "maroon",
               "yellow", "olive", "lime", "green", "aqua", "teal", "blue",
               "navy", "fuchsia", "purple")

    def __init__(self, color="white"):
        """Constructor for Figure object

        Keyword arguments:
        color --> in the list contained in the attribute .palette
        """
        if str(color).lower() not in self.palette:
            raise ValueError("'{}' is incorrect color! \
To get list of colors use: .palette".format(color))
        else:
            self.color = color.lower()

    def set_color(self, color):
        """set_color(color)

        Method of Figure object.
        Setting up attribute "color" of object.
        "color" must be in the list contained in the attribute .palette
        If "color" not in list - raise ValueError
        """
        if str(color).lower() not in self.palette:
            raise ValueError("'{}' is incorrect color! \
To get list of colors use: {}.palette".format(color, self.__class__))
        else:
            self.color = color.lower()


class Oval_new(Figure_new):
    """class Oval(Figure)

    Create object oval - geometric figure
    """
    def __init__(self, height, width, color="white"):
        """Constructor for Oval object

        Keyword arguments:
        height --> (int)
        width --> (int)
        color --> in the list contained in the attribute .palette
        """
        Figure_new.__init__(self, color)
        self.height = height
        self.width = width


class Square_new(Figure_new):
    """class Square(Figure)

    Create object square - geometric figure
    """
    def __init__(self, height, width, color="white"):
        """Constructor for Square object

        Keyword arguments:
        height --> (int)
        width --> (int)
        color --> in the list contained in the attribute .palette
        """
        Figure_new.__init__(self, color)
        self.height = height
        self.width = width


# -------------------------------- TESTS ----------------------------
def test1():
    a = Oval(10, 20)
    print(a.width, a.height, a.color)
    a.set_color("yellow")
    print(a.width, a.height, a.color)
    a.set_color("no color")


def test2():
    a = Oval_new(10, 20, "blue")
    print(a.width, a.height, a.color)
    a.set_color("green")
    print(a.width, a.height, a.color)
    a.set_color("no color")
