# -*- coding: utf-8 -*-
"""processcpu2plot Test"""

import pytest
#import sys
#import os
import processcpu2plot as pc2p
#sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


def test_empty_parameters():
    """ Tests the processcpu2plot creation without values
    """
    process = pc2p.ProcessCPU2Plot()


#class TestProcessCpu2Plot:
#  def test_empty_input_parameters(self):
# """ Tests empty input parameters """
# with pytest.raises(ValueError):
# pc2p.ProcessCPU2Plot()
