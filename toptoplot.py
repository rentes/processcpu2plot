#!/usr/bin/env python3
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

os.system("top -b -d 0.25 -n " + sys.argv[2] + " | grep -v \"top - \" | grep -w \"" + sys.argv[1] + "\" > top.txt")

values = []
with open("top.txt") as topfile:
    for line in topfile:
        values.append(line.split()[8])

t = np.arange(0., int(sys.argv[2]), 0.25)
plt.plot(values, 'bo')
plt.ylabel('process cpu %')
plt.xlabel('time: ' + sys.argv[2] + ' intervals of 0.25 each')
plt.axis([0, int(sys.argv[2]), 0, 100])
plt.show()

