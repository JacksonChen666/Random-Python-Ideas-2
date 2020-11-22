from itertools import permutations


def getUnscrambles(word, validWordsList: list):
    try:
        temp = [i for i in set(map(lambda a: "".join(a), permutations(word))) if i in validWordsList]
        if len(temp) > 0:
            return temp
        else:
            print("No words found!")
    except KeyboardInterrupt:
        print("Canceled")


def getWords():
    with open("words_alpha.txt") as f:
        return f.read().splitlines()


if __name__ == '__main__':
    validWords = getWords()
    while True:
        inp = input("Word to unscramble: ")
        if not inp:
            break
        words = getUnscrambles(inp, validWords) or None
        if words is None:
            continue
        print(f"{words}\n")
