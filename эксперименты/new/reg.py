# -*- coding:utf-8 -*-
import re
text = '<html><head><title></head></html>'
com = re.compile('<.*?>')
search = com.findall(text)
print()
