1. What gets printed?
x = 4.5
y = 2
print(x//y)
>> 2

2. What gets printed?
nums = set([1,1,2,3,3,3,4])
print(len(nums))
>> 4

3. What gets printed?
x = True
y = False
z = False

if x or y and z:
    print("yes")
else:
    print("no")

>> 'yes'

4. What gets printed?
x = True
y = False
z = False
if not x or y:
    print(1)
elif not x or not y and z:
    print(2)
elif not x or y or not y and x:
    print(3)
else:
    print(4)
>> 3

5. What gets printed?
counter = 1
def doLotsOfStuff():
    global counter
    for i in (1, 2, 3):
        counter += 1
doLotsOfStuff()
print(counter)
>> 4

6. What gets printed?
counter = 1
def doLotsOfStuff():
    counter = 1
    for i in (1, 2, 3):
        counter += 1
doLotsOfStuff()
print(counter)
>> 1

7. What gets printed?
name = "snow storm"
print(name[6:8])
>>'to'

8. What gets printed?
name = "snow storm"
name[5] = 'X'
print(name)
>> Error

9. What gets printed?
for i in range(2):
    print(i)
for i in range(4,6):
    print(i)
>>0
1
4
5

10. What gets printed?
country_counter = {}
def addone(country):
    if country in country_counter:
        country_counter[country] += 1
    else:
        country_counter[country] = 1
addone('China')
addone('Japan')
addone('china')
print(len(country_counter))

>>3
