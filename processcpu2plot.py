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

    External dependencies: pyplot (matplotlib), numpy and psutil
"""
import matplotlib.pyplot as plt
import numpy as np
import psutil
import sys


USAGE = "usage: processcpu2plot.py <process-name> " +\
        "<iterations> <interval>\n" +\
        "exiting."
INCORRECT_NUMBER_OF_PARAMETERS_FOUND = "incorrect number of parameters.\n" +\
                                       USAGE
NO_PROCESS_FOUND = "process not found. please check input parameters. " +\
                   "process name has to exactly match, e.g. chrome.exe " +\
                   "not chrome.EXE nor Chrome.exe"
INCORRECT_ITERATIONS_FOUND = "incorrect iterations parameter. " +\
                             "It must be an integer.\n" + USAGE
INCORRECT_INTERVAL_FOUND = "incorrect interval parameter. " +\
                           "It must be a float.\n" + USAGE


class ProcessCPU2Plot:
    """ The main class
    """

    def __init__(self, process, iterations, interval):
        self.process = process
        self.iterations = iterations
        self.interval = interval
        self.pids = []
        self.values = []

    def validate_parameters(self):
        """ Validates if there are parameters entered on the command line
        :param self: the processcpu2plot object
        """
        self.validate_process()
        self.validate_iterations()
        self.validate_interval()

    def validate_process(self):
        """ Validates the process name  parameter
        :return: the process name entered on the command line
        """
        process_found = False
        for process in psutil.process_iter():
            if process.name() == self.process:
                process_found = True
                break
        if process_found is False:
            print(NO_PROCESS_FOUND)
            exit(-1)

    def validate_iterations(self):
        """ Validates the iterations parameter
        :return: the iterations parameter entered on the command line
        """
        try:
            int(self.iterations)
        except ValueError:
            print(INCORRECT_ITERATIONS_FOUND)
            exit(-1)
        self.iterations = int(self.iterations)

    def validate_interval(self):
        """ Validates the interval parameter
        :return: the interval parameter entered on the command line
        Parameters after the interval parameters are neglected
        """
        try:
            float(self.interval)
        except ValueError:
            print(INCORRECT_INTERVAL_FOUND)
            exit(-1)
        self.interval = float(self.interval)

    def process_pid(self):
        """ Gets the list of the running process (entered on the command line) PIDs
        :param self: the processcpu2plot object
        :return: A list of the process PIDs
        """
        pids = []
        for _process in psutil.process_iter():
            if _process.name() == self.process:
                pids.append(psutil.Process(_process.pid))
        return pids

    def process_cpu_values(self):
        """ Gets the CPU % values from the running process PIDs
        :return: A list with the CPU % for each running process PID
        """
        # pylint: disable=no-member
        values_array = np.zeros((len(self.pids), self.iterations))
        # pylint: enable=no-member
        for iteration in range(self.iterations):
            for process_index in range(len(self.pids)):
                try:
                    self.pids[process_index].cpu_percent(interval=0.1)
                    values_array[process_index][iteration] = \
                        self.pids[process_index].cpu_percent(self.interval)
                except psutil.NoSuchProcess:
                    print('process with ID ' +
                          str(self.pids[process_index].pid) +
                          ' no longer running. setting cpu % to 0.0')
                    values_array[process_index][iteration] = 0.0
        return values_array

    def plot(self):
        """ Uses the matplotlib to create a line graphic plot
        """
        for pid_value in range(len(self.values)):
            plt.plot(self.values[pid_value], ':s',
                     label=str(self.pids[pid_value].pid))
        plt.ylabel(sys.argv[1] + ' CPU %')
        plt.xlabel('time: ' + str(self.iterations) + ' iterations of ' +
                   str(self.interval) + 's each')
        plt.axis([0, self.iterations, 0, 100])
        if len(self.pids) == 1:
            plt.legend(loc=1, ncol=2, shadow=True, title="PID", fancybox=True)
        else:
            plt.legend(loc=1, ncol=2, shadow=True, title="PIDs", fancybox=True)
        plt.show()


if __name__ == "__main__":
    NUMBER_OF_PARAMETERS = len(sys.argv) - 1
    if NUMBER_OF_PARAMETERS < 3:
        print(INCORRECT_NUMBER_OF_PARAMETERS_FOUND)
        exit(-1)
    # creates a new ProcessCPU2Plot object given the command line parameters
    PROCESSCPU = ProcessCPU2Plot(sys.argv[1], sys.argv[2], sys.argv[3])
    PROCESSCPU.validate_parameters()
    # obtains the process PID(s), its CPU % values and plots them
    PROCESSCPU.pids = PROCESSCPU.process_pid()
    PROCESSCPU.values = PROCESSCPU.process_cpu_values()
    PROCESSCPU.plot()
