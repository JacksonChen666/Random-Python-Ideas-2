"""How this works is that it takes the word, turn it into definitions, and repeat as many as wanted.
Dictionary from https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json"""
import json
import os

import requests as r

if __name__ == '__main__':
    if not os.path.exists("dictionary.json"):
        dictionary = r.get("https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json")
        with open("dictionary.json", "w") as f:
            f.write(dictionary.text)

    with open("dictionary.json") as f:
        dictionary = json.load(f)

    inText = input("What would you like to convert into something bigger?\n> ")

    inText = inText.split(" ")

    dictionary_keys = dictionary.keys()
    for i in range(len(inText)):
        text = inText[i]
        if text in dictionary_keys:
            inText[i] = dictionary[text]

    inText = " ".join(inText)
    print(f"Here is what's left:\n{inText}")
