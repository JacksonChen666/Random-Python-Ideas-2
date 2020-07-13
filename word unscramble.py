from random import shuffle

maxLen = 0
minLen = 100


def getUnscrambles(word, validWordsList: list, gen=1000, retries=3):
    global maxLen, minLen
    if len(word) > maxLen or len(word) < minLen:
        print("Too short or too long!")
        return
    temp = [word]
    tempWord = list(word)
    try:
        for r in range(retries):
            for w in range(gen):
                shuffle(tempWord)
                temp.append("".join(tempWord))
            temp = [i for i in list(dict.fromkeys(temp)) if i in validWordsList]
            if len(temp) > 0: return temp
        else:
            print("No words found!")
    except KeyboardInterrupt:
        print("Canceled")

def getWords():
    global maxLen, minLen, validWords
    with open("words_alpha.txt") as f:
        validWords = f.read().splitlines()
        maxLen = len(max(validWords))
        minLen = len(min(validWords))
    return validWords


if __name__ == '__main__':
    validWords = getWords()
    while True:
        inp = input("Word to unscramble: ")
        if not inp: break
        words = getUnscrambles(inp, validWords) or None
        if words is None: continue
        print(f"{words}\n")
