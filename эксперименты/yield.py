#-*- encoding: utf-8 -*-


def accumulate():
    tally = 0
    while 1:
        next = yield
        print("accumulate "+str(next))
        if next is None:
             return tally
        tally += next


def gather_tallies(tallies):
    while 1:
         tally = yield from accumulate()
         print(tally)
         tallies.append(tally)

tallies = []
acc = gather_tallies(tallies)
next(acc)  # Ensure the accumulator is ready to accept values
for i in range(4):
    print(acc.send(i))
acc.send(None)  # Finish the first tally

for i in range(5):
     acc.send(i)
acc.send(None)  # Finish the second tally
tallies