# -*- coding: utf-8 -*-
"""processcpu2plot Test"""
import pytest
from .. import processcpu2plot as pc2p


def test_iterations():
    """ Tests the cration of ProcessCPU2Plot objects with invalid iterations
    Invalid iterations include:
    - strings
    - float numbers
    - integers equal to or less than zero
    """
    process = pc2p.ProcessCPU2Plot('chrome', 'test', 1)
    with pytest.raises(SystemExit):
        process.validate_iterations()
    process = pc2p.ProcessCPU2Plot('chrome', '0.1', 1)
    with pytest.raises(SystemExit):
        process.validate_iterations()
    process = pc2p.ProcessCPU2Plot('chrome', '0', 1)
    with pytest.raises(SystemExit):
        process.validate_iterations()
    process = pc2p.ProcessCPU2Plot('chrome', '-1', 1)
    with pytest.raises(SystemExit):
        process.validate_iterations()


def test_interval():
    """ Tests the creation of ProcessCPU2Plot objects with invalid interval
    Invalid intervals include:
    - strings
    - integers (or floats) equal to or less than zero
    """
    process = pc2p.ProcessCPU2Plot('chrome', '1', 'a')
    with pytest.raises(SystemExit):
        process.validate_interval()
    process = pc2p.ProcessCPU2Plot('chrome', '1', '0.0')
    with pytest.raises(SystemExit):
        process.validate_interval()
    process = pc2p.ProcessCPU2Plot('chrome', '1', '-2.3')
    with pytest.raises(SystemExit):
        process.validate_interval()
