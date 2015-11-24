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


USAGE = "usage: processcpu2plot.py <process-name> " +\
        "<iterations> <interval>\n" +\
        "exiting."
INCORRECT_NUMBER_OF_PARAMETERS_FOUND = "incorrect number of parameters found.\n" + USAGE

NO_PROCESS_FOUND = "process not found. please check input parameters. " +\
                   "process name has to exactly match, e.g. chrome.exe " +\
                   "not chrome.EXE nor Chrome.exe"
INCORRECT_ITERATIONS_FOUND = "incorrect iterations parameter. It must be an integer.\n" + USAGE
INCORRECT_INTERVAL_FOUND = "incorrect interval parameter. It must be a float.\n" + USAGE


class ProcessCPU2Plot:
    """ The main class
    """

    def __init__(self, process, iterations, interval):
        self.process = process
        self.iterations = iterations
        self.interval = interval

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

    def process_cpu_values(self, _process, _iterations, _interval):
        """ Gets the CPU % values from the running process PIDs
        :param _process: The list of process PIDs
        :param _iterations: How many iterations will be to obtain CPU % values
        :param _interval: How long each iteration will last in seconds
        :return: A list with the CPU % for each running process PID
        """
        values_array = [[0 for x in range(_iterations)]
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

    def plot(self, _values, _pids, _iterations, _interval):
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
    number_of_parameters = len(sys.argv) - 1
    if number_of_parameters < 3:
        print(INCORRECT_NUMBER_OF_PARAMETERS_FOUND)
        exit(-1)
    proc = ProcessCPU2Plot(sys.argv[1], sys.argv[2], sys.argv[3])
    proc.validate_parameters()
    pids = proc.process_pid()
    values = proc.process_cpu_values(pids, proc.iterations, proc.interval)
    proc.plot(values, pids, proc.iterations, proc.interval)

