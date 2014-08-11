import time
from datetime import datetime

d1 = datetime.now()
t1 = time.time()
time.sleep(3)
d2 = datetime.now()
t2 = time.time()
dt = t2 - t1
dd = (d2 - d1).total_seconds()
print(dt, dd)
