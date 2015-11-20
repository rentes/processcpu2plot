#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
import psutil

pid = 0
process_cpu_percent = 0.0
values = []
if sys.argv[1]:
    for process in psutil.process_iter():
        if process.name() == sys.argv[1]:
            # TODO: cycle through all possible forks
            pid = process.pid

process = psutil.Process(pid)
print(process)
for i in range(10):
    process_cpu_percent = process.cpu_percent(interval=1)
    print(process_cpu_percent)
    values.append(process_cpu_percent)

plt.plot(values, 'b')
plt.ylabel('process cpu %')
plt.xlabel('time: s')
plt.axis([0, 10, 0, 100])
plt.show()