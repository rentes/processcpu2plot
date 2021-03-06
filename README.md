[![Build Status](https://travis-ci.org/rentes/processcpu2plot.svg?branch=master)](https://travis-ci.org/rentes/processcpu2plot) [![License](https://go-shields.herokuapp.com/license-MIT-blue.png)](http://opensource.org/licenses/MIT)

# processcpu2plot
A python command-line utility to display CPU % output of a single process as a graphic plot.

<img src="img/figure_1.png" />

## Usage

Just run it on the command line like this:

```python
python processcpu2plot.py <process-name> <total number of iterations> <interval>
```
- The process name must match the process name you want to plot its CPU usage
- The number of iterations is an integer with the number of iterations you want to check for the process CPU usage
- The interval is a float value (2 decimal places) of how long each iteration will last

Examples

On Linux/Mac OS:
```python
$ python processcpu2plot.py chrome 21 0.1
```

On Windows:
```python
$ python processcpu2plot.py chrome.exe 21 0.1
```

## Installation Instructions

This piece of software is specifically made for Python 3.4.

### Windows

Install Python 3.4, matplotlib and its dependencies. It's best to install any scipy-stack compatible Python distributions, 
like Anaconda. See [1].

### Linux/Mac OS X

Install Python 3.4 and then matplotlib using pip.

## Testing

The test suite uses pytest. All you have to do is run it like this:

```python
$ py.test
```

## TODO

- ~~Treat all process forks separately on the plot with a different color~~
- mouse hover a plot line will show the process ID and CPU % on that point.
- add a color palette on the legend where different PIDs never have the same color.
- after each iteration, add the new forked processes (if any), and remove the non-existing ones (if any).
- expand utility to other metrics: memory, disk I/O, or number of open file descriptors, for example. Pass these options as a command line parameter.

## Resources

1. <a href="http://matplotlib.org/users/installing.html">Matplotlib installation instructions</a>
2. <a href="http://pythonhosted.org/psutil/#process-class">psutil documentation (Process class)</a>