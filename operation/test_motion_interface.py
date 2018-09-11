"""
@author: Ian Huang

This is the unit test for the motion interface.
"""
import unittest
from test_controllerSendRecv import TesterPort

class TestAngleCommander(unittest.TestCase):
    def test_get_initial_state(self):
        pass
    def test_checkAngleLimits(self):
        pass
    def test_goTo(self):
        pass
    def test_getCubicSmoothing(self):
        pass
    def test_writeLine(self):
        pass
    def test_writePosTransLine(self):
        pass
    def test_writeImageLine(self):
        pass
    def test_writeVideoLine(self): 
        pass
    def logState(self):
        pass
    def imageCapture(self): 
        pass

if __name__=='__main__':
    unittest.main()
