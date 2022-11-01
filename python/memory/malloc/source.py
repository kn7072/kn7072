#coding: utf-8

# https://habr.com/ru/post/479744/

iterations = 2000000

l = []
for i in range(iterations):
    l.append(None)
        
for i in range(iterations):
    l[i] = {}

# s = []  # [1]
# s = l[::2]  # [2]
# s = l[2000000 // 2::]  # [3]
s = l[::100]  # [4]

for i in range(iterations):
    l[i] = None        
        
for i in range(iterations):
    l[i] = {}


# PYTHONMALLOCSTATS="True" && python3 source.py 2>result.txt