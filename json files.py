import json

with open("solves.json") as f:
    jsonData = json.load(f)

print(jsonData)
