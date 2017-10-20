# 5. Write a script to convert decimal to hexadecimal
#         Sample decimal number: 30, 4
#         Expected output: 1e, 04

n = input("Enter an integer to convert from decimal to hexadecimal: ")
if not len(n):
    n = 0
else:
    try:
        n = int(n)
    except:
        print("You enter not integer!")
        exit(1)
print("Decimal {0}.\nHexadecimal {1}".format(n, hex(n)))
