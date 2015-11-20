# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import psutil
import sys

pid = 0
process_cpu_percent = 0.0
values = []

if len(sys.argv) == 1:
    print('no parameters input.\n' +
          'usage: toptoplot.py <process-name> <iterations> <interval>\n' +
          'exiting.')
    exit(0)

if sys.argv[1]:
    for process in psutil.process_iter():
        if process.name() == sys.argv[1]:
            # TODO: cycle through all possible forks
            pid = process.pid

if pid == 0:
    print('process not found. please check input.' +
          'process name has to exactly match, e.g. chrome.exe not chrome.EXE')
    exit(0)

process = psutil.Process(pid)
print(process)

if len(sys.argv) >= 3:
    iterations = int(sys.argv[2])
else:
    iterations = 11
if len(sys.argv) == 4:
    interval = float(sys.argv[3])
else:
    interval = 1.0

try:
    for i in range(iterations):
        process_cpu_percent = process.cpu_percent(interval)
        print(process_cpu_percent)
        values.append(process_cpu_percent)
except psutil.NoSuchProcess:
    print('process no longer running. exiting')
    exit(-1)

plt.plot(values, 'b')
plt.ylabel('process cpu %')
plt.xlabel('time: s')
plt.axis([0, iterations, 0, 100])
plt.show()
