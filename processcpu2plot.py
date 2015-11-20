# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import psutil
import sys


def validate_iterations():
    param = 0
    if len(sys.argv) == 1:
        print('no parameters input.\n' +
              'usage: processcpu2plot.py <process-name> ' +
              '<iterations> <interval>\n' +
              'exiting.')
        exit(0)
    if len(sys.argv) >= 3:
        param = int(sys.argv[2])
    else:
        param = 11
    return param


def validate_interval():
    param = 0
    if len(sys.argv) == 4:
        param = float(sys.argv[3])
    else:
        param = 1.0
    return param


def process_pid():
    _pid = 0
    if sys.argv[1]:
        for _process in psutil.process_iter():
            if _process.name() == sys.argv[1]:
                # TODO: cycle through all possible forks
                _pid = _process.pid
    if _pid == 0:
        print('process not found. please check input.' +
              'process name has to exactly match, e.g. chrome.exe ' +
              'not chrome.EXE nor Chrome.exe')
        exit(0)
    return _pid


def process_cpu_values(_iterations, _interval):
    values_array = []
    try:
        for i in range(_iterations):
            process_cpu_percent = process.cpu_percent(_interval)
            print(process_cpu_percent)
            values_array.append(process_cpu_percent)
    except psutil.NoSuchProcess:
        print('process no longer running. exiting')
        exit(-1)
    return values_array


def plot(_values, _process, _iterations, _interval):
    plt.plot(_values, 'b')
    plt.ylabel(_process.name() + ' CPU %')
    plt.xlabel('time: ' + str(_iterations) + ' iterations of ' +
               str(_interval) + 's each')
    plt.axis([0, _iterations, 0, 100])
    plt.show()


if __name__ == "__main__":
    pid = 0
    values = []
    iterations = 0
    interval = 0.0

    iterations = validate_iterations()
    interval = validate_interval()
    pid = process_pid()
    process = psutil.Process(pid)
    values = process_cpu_values(iterations, interval)
    plot(values, process, iterations, interval)
