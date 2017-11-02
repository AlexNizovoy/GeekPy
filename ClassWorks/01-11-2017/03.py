def conv(temp=None, base="Celsius"):
    if not temp:
        return None
    if base == "Celsius":
        return temp * 9 / 5 + 32
    else:
        return (temp - 32) * 5 / 9


cels = float(input("In Celsius:"))
fahr = float(input("In Fahrenheit:"))

print("{0}C is {1} in Fahrenheit".format(cels, conv(cels)))
print("{0}F is {1} in Celsius".format(fahr, conv(fahr, "Fahrenheit")))
