import random

for i in range(10):
    string = "random cutting string"
    index = random.randint(0, len(string) - 1)
    string = string[index:index + 1]

    print(string, end="")
