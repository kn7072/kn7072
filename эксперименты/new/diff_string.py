# -*- coding:utf-8 -*-
import difflib
d = difflib.Differ()
text1_lines = r'член  КвИТуй  (ОБЩСТВО ФИНАНсС хер С ОГРАНИЧЕОЙ  ОцТВЕТСТВЕННОСТЮ  ФИНАНС' # ФИкНАНС
text2_lines = r'КИТ ФИНАНС (ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ'
diff = d.compare(text1_lines, text2_lines)
# for i in diff:
#     print(i)
print('\n'.join(diff))
print()


def print_x(test: str) -> str:
    """

    """
    print(test)


print_x("qdff")

