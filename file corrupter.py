import os
import random
from sys import argv

with open(argv[1], "rb") as f:
    temp = f.read()

max_size = int(argv[2])

for i in range(int(argv[3])):
    a = random.randint(0, max_size)
    b = 0
    while a > b:
        b = random.randint(0, max_size)
    data = temp[a:b]
    size = len(data)
    data = int.from_bytes(data, "big")
    if random.randint(0, 1):
        data <<= random.randint(1, 1024)
    else:
        data >>= random.randint(1, 1024)
    data = hex(data)[2:]
    data.zfill(size * 2)
    try:
        data = bytes.fromhex(data)
    except ValueError:
        continue
    if data == 0:
        continue
    temp = temp[a:] + data + temp[len(temp) - len(data) + random.randint(0, 10):b]

name = argv[1].rpartition(os.extsep)
with open(f"{name[0]}_CORRUPTED{''.join(name[1:])}", "wb") as f:
    f.write(temp)
