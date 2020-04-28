import random, re


def words(wordsAmount):
    global dictionary
    wordsAmount: int
    words = []
    for w in range(int(wordsAmount)):
        words.append(str(random.choice(dictionary)))
    return words


def sentences(sentencesAmount, wordsAmount):
    global dictionary
    sentencesAmount: int
    wordsAmount: int
    sentence = ""
    sentences = []
    for s in range(int(sentencesAmount)):
        for w in range(int(wordsAmount)):
            sentence += str(random.choice(dictionary)) + " "
        sentence = sentence[:-1]
        sentence += "."
        sentences.append(sentence)
        sentence = ""
    return sentences


def paragraphs(paragraphsAmount, sentencesAmount, wordsAmount):
    global dictionary
    paragraphsAmount: int
    sentencesAmount: int
    wordsAmount: int
    paragraphsList = []
    sentence = ""
    for p in range(int(paragraphsAmount)):
        for s in range(int(sentencesAmount)):
            for w in range(random.randint(wordsAmount - 3, wordsAmount + 3)):
                sentence += str(random.choice(dictionary)) + " "
            sentence = sentence[:-1]
            sentence += random.choice([". ", ", "])
        sentence = sentence[:-1]
        if sentence.endswith(","):
            sentence = sentence[:-1]
            sentence += ". "
        if sentence.endswith(". "):
            sentence = sentence[:-1]
        paragraphsList.append(sentence)
    return paragraphsList


def validWord():
    global dictionary
    while True:
        word = str(input("What word do you think is valid?\n"))
        for i in dictionary:
            if word.lower() == i.lower():
                print("It's a word!\n{} is valid".format(word))
                continue


with open("words_alpha.txt") as r:
    dictionary = r.read().split("\n")
    print("There are {} words".format(len(dictionary)))

if __name__ == "__main__":
    validWord()
