# -*- coding: utf-8 -*-
""" processcpu2plot: a python command line utility to display CPU % output
    of a single process as a graphic plot.

    Synapsis:

    $ processcpu2plot <process> <nr iterations> <duration of iteration>

    Example:

    $ processcpu2plot chrome 21 0.1
    (For Mac OS/Linux)

    $ processcpu2plot chrome.exe 21 0.1
    (For Windows)

    Runs 21 iterations of 0.1s each to obtain the CPU % values for the
    chrome processes and generates a line plot for each at the end

    External dependencies: pyplot (matplotlib), and psutil
"""
import matplotlib.pyplot as plt
import psutil
import sys


def validate_iterations():
    """ Validates the iterations parameter
    :return: the iterations parameter entered on the command line
    """
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
    """ Validates the interval parameter
    :return: the interval parameter entered on the command line
    """
    if len(sys.argv) == 4:
        param = float(sys.argv[3])
    else:
        param = 1.0
    return param


def process_pid():
    """ Gets the list of the running process (entered on the command line) PIDs
    :return: A list of the process PIDs
    """
    pids = []
    if sys.argv[1]:
        for _process in psutil.process_iter():
            if _process.name() == sys.argv[1]:
                pids.append(psutil.Process(_process.pid))
    if len(pids) == 0:
        print('process not found. please check input.' +
              'process name has to exactly match, e.g. chrome.exe ' +
              'not chrome.EXE nor Chrome.exe')
        exit(0)
    return pids


def process_cpu_values(_process, _iterations, _interval):
    """ Gets the CPU % values from the running process PIDs
    :param _process: The list of process PIDs
    :param _iterations: How many iterations will be to obtain CPU % values
    :param _interval: How long each iteration will last in seconds
    :return: A list with the CPU % for each running process PID
    """
    values_array = [[-1 for x in range(_iterations)]
                    for x in range(len(_process))]
    for iteration in range(_iterations):
        for process_index in range(len(_process)):
            try:
                values_array[process_index][iteration] = \
                    _process[process_index].cpu_percent(_interval)
            except psutil.NoSuchProcess:
                print('process with ID ' + str(_process[process_index].pid) +
                      ' no longer running. setting cpu % to 0.0')
                values_array[process_index][iteration] = 0.0
    return values_array


def plot(_values, _pids, _iterations, _interval):
    """ Uses the matplotlib to create a line graphic plot
    :param _values: the list of CPU % values
    :param _pids: the list of PIDs (for the label on the graphic plot)
    :param _iterations: How many iterations will be
    :param _interval: How long each iteration lasts
    """
    for pid_value in range(len(_values)):
        plt.plot(_values[pid_value], label=str(_pids[pid_value].pid))
    plt.ylabel(sys.argv[1] + ' CPU %')
    plt.xlabel('time: ' + str(_iterations) + ' iterations of ' +
               str(_interval) + 's each')
    plt.axis([0, _iterations, 0, 100])
    if len(_pids) == 1:
        plt.legend(loc=1, ncol=2, shadow=True, title="PID", fancybox=True)
    else:
        plt.legend(loc=1, ncol=2, shadow=True, title="PIDs", fancybox=True)
    plt.show()


if __name__ == "__main__":
    ITERATIONS = validate_iterations()
    INTERVAL = validate_interval()
    PIDS = process_pid()
    VALUES = process_cpu_values(PIDS, ITERATIONS, INTERVAL)
    plot(VALUES, PIDS, ITERATIONS, INTERVAL)
