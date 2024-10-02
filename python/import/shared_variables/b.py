import sys
from a import change_a, print_a, add_c

print_a()
change_a("10")
print_a()

print(sys.modules.keys())
print("#"*20)
add_c()
print(sys.modules.keys())
print()

