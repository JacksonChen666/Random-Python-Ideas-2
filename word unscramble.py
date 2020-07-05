from random import shuffle


def getUnscrambles(word, validWordsList: list, gen=1000, retries=3, maxLen=None, minLen=None):
    if not maxLen: maxLen = len(max(validWordsList))
    if not minLen: minLen = len(min(validWordsList))
    if len(word) > maxLen or len(word) < minLen:
        print("Too short or too long!")
        return
    temp = []
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
            return
    except KeyboardInterrupt:
        print("Canceled")
        return


if __name__ == '__main__':
    with open("words_alpha.txt") as f:
        validWords = f.read().splitlines()
    while True:
        inp = input("Word to unscramble: ")
        if not inp: break
        words = getUnscrambles(inp, validWords)
        print(words)
