import os
import re

import html2text
import requests

text = html2text.html2text(requests.get(
    "https://hypixel-skyblock.fandom.com/wiki/Fairy_Souls").text[:-9500])


def regex(a):
    return re.compile(f'({a + "-" if a else ""}\d+) +\| +(-?\d+ +\| +-?\d+ +\| +-?\d+)')


def template(x, y, z):
    global count
    count += 1
    return f'waypoint:{count}:{count}:{x}:{y}:{z}:12:false:0:gui.xaero_default:false:0:false'


count = 0
prefixes = {
    'All': '',  # i can't figure out how to filter stuff that doesn't belong
    'The Barn': 'Brn',
    'Mushroom Desert': 'MD',
    'Gold Mine': 'GM',
    'Deep Caverns': 'DC',
    "Spider's Den": 'SD',
    'Blazing Fortress': 'BF',
    'The End': 'End',
    'The Park': 'Park',
    "Jerry's Workshop": 'JW',
    'Dungeon Hub': 'DH'
}

os.mkdir("Hypixel Skyblock Fairy Souls")
os.chdir("Hypixel Skyblock Fairy Souls")

with open("config.txt", "w") as f:
    f.write("""usingMultiworldDetection:true
ignoreServerLevelId:false
teleportationEnabled:false
usingDefaultTeleportCommand:true
sortType:NONE
sortReversed:false""")

for i in prefixes.keys():
    count = 0
    prefix = prefixes[i]
    os.mkdir(i)
    os.chdir(i)
    temp = list(map(lambda a: template(*(int(i)
                                         for i in a[1].split("  | "))), regex(prefix).findall(text)))
    print(i)
    print(temp)
    with open("mw4,0,5_1.txt", "w") as f:
        f.write("\n".join(temp))
    os.chdir("../")
