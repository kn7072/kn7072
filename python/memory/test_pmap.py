# -*- coding: utf-8 -*-

import os
import random
import time

delay = 10
print(f"start {os.getpid()}")
time.sleep(delay)


count_instance = 10000000

print(f"Создаю {count_instance} объектов")
temp_dict = {random.randint(0, 100000): i for i in range(count_instance)}
time.sleep(delay * 18)
