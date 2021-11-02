# -*- coding: utf-8 -*-


def accumulate():
    tally = 0
    while 1:
        x = yield
        if x is None:
            return tally
        tally += x


def gather_tallies(tallies):
    while 1:
        tally = yield from accumulate()
        print(tally)
        tallies.append(tally)

tallies = []
acc = gather_tallies(tallies)
next(acc)  # Ensure the accumulator is ready to accept values

for i in range(4):
    acc.send(i)
acc.send(None)  # Finish the first tally

for i in range(5):
    acc.send(i)
acc.send(None)  # Finish the second tally
tallies