from turtle import *
import random
turtle = Turtle()
turtle.hideturtle()
screen = Screen()
screen.setup(width=.75, height=.75, startx=0, starty=0)
screen.bgcolor('orange')


def make_dots(start, size, color, limit, step):
    start = start
    for i in range(limit):
        turtle.goto(screen.window_height() * size, start)
        turtle.dot(random.randint(10, 15), color)
        start -= step


def make_center(start, color, limit, step):
    start = start
    for i in range(limit):
        turtle.goto(0, start)
        turtle.dot(random.randint(10, 15), color)
        start -= step


turtle.penup()
make_dots(200, 0.75, 'purple', 5, 50)
make_dots(200, 0.5, 'white', 5, 50)
make_dots(200, 0.25, 'blue', 5, 50)
make_center(200, 'white', 5, 50)
make_dots(200, -0.25, 'purple', 8, 50)
make_dots(200, -0.5, 'white', 8, 50)
make_dots(200, -0.75, 'blue', 8, 50)
make_dots(200, -0.62, 'green', 7, 50)
make_dots(200, -0.38, 'red', 7, 50)
make_dots(200, -0.12, 'green', 4, 50)
make_dots(200, 0.12, 'red', 4, 50)
make_dots(200, 0.38, 'green', 4, 50)
make_dots(200, 0.62, 'red', 4, 50)
turtle.goto(0, screen.window_width()*-0.12)
turtle.write('2018 Happy New Year!', font=('Arial', 20, 'normal'))
turtle.goto(0, screen.window_width()*-0.15)
turtle.write('Woof! Woof!', font=('Arial', 10, 'normal'))
turtle.pendown()
done()
