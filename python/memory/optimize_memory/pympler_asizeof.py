# -*- coding: utf-8 -*-

# https://towardsdatascience.com/optimizing-memory-usage-in-python-applications-f591fc914df5
# https://gist.github.com/MartinHeinz/eee3a88e53d516b8c47be589404a44ce

# pip install pympler
from pympler import asizeof
print(asizeof.asizeof([1, 2, 3, 4, 5]))
# 256

print(asizeof.asizeof((1, 2, 3, 4, 5)))
# 240

print(asizeof.asized([1, 2, 3, 4, 5], detail=1).format())
# [1, 2, 3, 4, 5] size=256 flat=96
#     1 size=32 flat=32
#     2 size=32 flat=32
#     3 size=32 flat=32
#     4 size=32 flat=32
#     5 size=32 flat=32

print(asizeof.asized((1, 2, 3, 4, 5), detail=1).format())
# (1, 2, 3, 4, 5) size=240 flat=80
#     1 size=32 flat=32
#     2 size=32 flat=32
#     3 size=32 flat=32
#     4 size=32 flat=32
#     5 size=32 flat=32

print(asizeof.asized([1, 2, [3, 4], "string"], detail=1).format())
# [1, 2, [3, 4], 'string'] size=344 flat=88
#     [3, 4] size=136 flat=72
#     'string' size=56 flat=56
#     1 size=32 flat=32
#     2 size=32 flat=32