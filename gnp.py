from random import random, seed
from math import log
import sys

def gnp(N, p):
    t = 0
    N2 = N * N
    while True:
        k = int(log(1 - random()) / log(1 - p))
        t += k
        if t >= N2:
            break;
        i, j = t % N, t / N;
        if i < j:
            print "D", i, j
        t += 1

if len(sys.argv) < 4:
   print sys.argv[0], "<N>", "<d>", "<seed>"
   exit()
N = int(sys.argv[1])
c = float(sys.argv[2])
seed(int(sys.argv[3]))
gnp(N, c/N)
