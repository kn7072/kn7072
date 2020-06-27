from collections import defaultdict

d1 = {'a': 7, 'b': -3, 'c': 1, 'd': 1}
d2 = {'a': 90, 'b': 89, 'x': 45, 'd': 90}
l = 90

# The default (==0) is a substitute for the condition "not in d2"
# As daniel suggested, it would be better if d2 itself was a defaultdict
d3 = defaultdict(int, d2)
x = [(k, d3[k]) for k in d1 if d3[k] < l]
######################################################
dic1 = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
dic2 = {'a':1, 'b':2, 'c':3, 'd':5}
dict3 = dict([x for x in dic1.items() if x not in dic2.items()])
print()