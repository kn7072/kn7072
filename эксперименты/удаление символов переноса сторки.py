# -*- coding:utf-8 -*-

import codecs

#f = codecs.open(r'file.txt', errors='')
f = open(r'file.txt').read()
new_f = f.replace('\n', '')
b = new_f.encode()
print()