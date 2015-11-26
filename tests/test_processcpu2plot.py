# -*- coding: utf-8 -*-
"""processcpu2plot Test"""
import pytest
from .. import processcpu2plot as pc2p


def test_processcpu2plot_iterations():
    """ Tests the cration of ProcessCPU2Plot objects with invalid iterations
    Invalid iterations include:
    - strings
    - float numbers
    - integers equal to or less than zero
    """
    proc = pc2p.ProcessCPU2Plot('chrome', 'test', 1)
    with pytest.raises(SystemExit):
        proc.validate_iterations()
    proc = pc2p.ProcessCPU2Plot('chrome', '0.1', 1)
    with pytest.raises(SystemExit):
        proc.validate_iterations()
    proc = pc2p.ProcessCPU2Plot('chrome', '0', 1)
    with pytest.raises(SystemExit):
        proc.validate_iterations()
    proc = pc2p.ProcessCPU2Plot('chrome', '-1', 1)
    with pytest.raises(SystemExit):
        proc.validate_iterations()
