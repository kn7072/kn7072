import sys
import inspect
# from package.sub_package_2 import sub_module_2
# sub_module_2.x()
sys.path
sys.modules

class B():
    b = 10
    pass
obj = B()
obj2 = B
for x in sys.modules:
    if x == 'package.sub_package_2.sub_module_2':
        print("package.sub_package_2.sub_module_2")
from package.sub_package_2 import sub_module_2
sub_module_2.x(obj2, obj)
for x in sys.modules:
    if x == 'package.sub_package_2.sub_module_2':
        print("package.sub_package_2.sub_module_2")
sys.meta_path  # Содержит список экземпляров искателей. По умолчанию пустой.