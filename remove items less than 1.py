# from https://www.geeksforgeeks.org/python-remove-elements-of-list-that-are-repeated-less-than-k-times/
from collections import Counter


def removeElements(lists, count):
    return [item for item in lists if Counter(lists)[item] >= count]


# Driver code 
lst = sorted([1, 1, 1, 2, 3, 2, 3, 4, 3, 2, 1, 0])
print(removeElements(lst, 2))
