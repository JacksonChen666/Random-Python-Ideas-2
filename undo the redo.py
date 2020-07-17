from random import choice, randint

prefix, suffix = "Did you ", "?"
words = {
    "action": ["undo the", "redo the"],
    "result": ["undo", "redo", "redid", "undid"],
    "ending": ["which"],
}
loop = randint(2, len(words["action"]) ** len(words["result"]) ** len(words["ending"]))
maxLoops = 100


def create_sentence(maxLoop=maxLoops):
    sentence, currentLoop = [prefix], 0
    while loop > len(sentence):
        sentence = list(dict.fromkeys(
            sentence + [f"{choice(words['action'])} {choice(words['result'])}, {choice(words['ending'])} "]
        ))
        currentLoop += 1
        if maxLoop < currentLoop: break
    return "".join(sentence).rstrip(", which") + suffix


if __name__ == '__main__':
    for i in range(1000):
        print(create_sentence(1000))
