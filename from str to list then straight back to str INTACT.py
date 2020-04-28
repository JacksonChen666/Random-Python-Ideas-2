from re import findall

if __name__ == '__main__':
    thing = findall(".", str(input("Text\n")))
    text = ""
    for i in thing:
        text += i
    print(text)
