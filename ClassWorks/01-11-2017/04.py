from random import randint


numb = randint(1, 9)
while True:
    i = int(input("Guess a number in [1, 9]:"))
    if i == numb:
        print("Well guessed!")
        break
    else:
        print("Guess again!")
