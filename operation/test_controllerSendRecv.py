"""
@author: Ian Huang
The test for the send, recv, and validate
"""
import unittest
import numpy as np
from controllerSendRecv import angle_string_maker, angle_string_parser
from controllerSendRecv import send, recv, validate

class TesterPort(object):
    def __init__(self, parser, strencoder):
        self.parser = parser
        self.data = None
        self.strencoder = strencoder

    def write(self, line):
        self.data = self.parser(line)

    def readline(self):
        return self.strencoder(self.data)

class TestControllerSendRecv(unittest.TestCase):
    
    def test_validate(self):
        """ testing validate """
        port = TesterPort(parser=angle_string_parser,
                        strencoder= angle_string_maker)
        angles1 = [12, 13, 14, 15, 16, 17]
        angles2 = np.array([float(item) for item in angles1])
        self.assertTrue(validate(angles1, angles2))

    def test_send(self):
        """ testing send"""
        # creating port
        port = TesterPort(parser=angle_string_parser,
                        strencoder= angle_string_maker)
        angles = [12, 13, 14, 15, 16, 17]
        send(angles, port, ang_str_encoder=angle_string_maker)
        self.assertEqual(angles, port.data, 
                msg='Test for send failed: {} and {} do not match'.\
                    format(angles, port.data))

    def test_recv(self):
        """ testing recv """
        port = TesterPort(parser=angle_string_parser,
                        strencoder= angle_string_maker)
        port.data = [12, 13, 14, 15, 16, 17]
        recved = recv(port, ang_str_decoder=angle_string_parser)
        self.assertEqual(port.data, recved,
                    msg='Test for recv failed: {} and {} do not match.'.\
                    format(port.data, recved))

if __name__=='__main__':
    # tests send and recv
    unittest.main()
