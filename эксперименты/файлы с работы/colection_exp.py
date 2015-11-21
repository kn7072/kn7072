# -*- encoding:utf-8 -*-
import collections
from collections import defaultdict, OrderedDict, namedtuple
s = "yeah but no but yeah but no but yeah"
words = s.split()
wordlocations = defaultdict(list)
for n, w in enumerate(words):
    print(n, w)
    wordlocations[w].append(n)

print(wordlocations)
################################################
d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}
x = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
print(x)
print(x['orange'])
################################################
Point = namedtuple('Point_x', ['x', 'y'])
p = Point(x=1, y=2)
print()


