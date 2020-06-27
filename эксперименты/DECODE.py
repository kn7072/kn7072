# -*- coding: UTF-8 -*-

testline = "строка с русскими символами и english letters"
print(testline.encode('utf-8'))
testline.encode('utf-8').decode('utf-8')  # utf-8

a = u'1\u0430'

print(testline)