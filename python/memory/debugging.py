# -*- coding: utf-8 -*-

import os
import signal
import sys
import time    

# https://stackoverflow.com/questions/25308847/attaching-a-process-with-pdb


def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)    


def print_log():
    print("START print_log")
    time.sleep(5)
    print("END print_log")


def loop():
    while True:
        x = 'foo'
        time.sleep(2)
        print_log()


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, handle_pdb)
    print(os.getpid())
    loop()