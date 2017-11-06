import re

question_re = re.compile(r"^\d+\.")

quiz = open('quiz_your_name.txt')
answ = open('answears.txt')
answ_obj = {}
key = 0
value = ""
start_exerc = False
result = 0
correct = {}
incorrect = {}

for line in answ.readlines():
    key, value = line.split("=")
    answ_obj[key] = value.strip()

for line in quiz.readlines():
    # check for starts some digits ends dot and endswith "?"
    find_reg = question_re.findall(line)
    if len(find_reg) and line.endswith("?\n"):
        key = find_reg[0][:-1]
        start_exerc = True
    if start_exerc:
        # check for ">>"
        if line.startswith(">>"):
            value = line[2:].strip()
            value = value.replace("\"", "")
            if answ_obj.get(key).lower() == value.lower():
                correct[key] = value
                result += 1
            else:
                incorrect[key] = value
            start_exerc = False
print("answers", answ_obj)
print("correct", correct)
print("incorrect", incorrect)
answ.close()
quiz.close()
print("Result: {}".format(result))
