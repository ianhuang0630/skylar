"""
@author: Ian Huang
This script implements the lower level API for sending and recving commands 
from the raspberry pi to the arduino through serial communication
"""

import numpy as np
import scipy as sp
import time

WAIT_MILLIS = 10

def angle_string_maker(angle_list):
    return ','.join(angle_list)
def angle_string_parser(angle_line):
    data = [int(element.strip()) for element in data_line.split(',')]
    return data

def send(angle_vec, serial_port):
    """ Function to send a vector of angles to the arduino
    Args:
        angle_vec: list or numpy array of the joint angles
        serial_port: the port that you would like to send data to.
    Returns:
        True if the communication was successful, false if it wasn't
    """
    if not isinstance(angle_vec, list) and \
            not isinstance(angle_vec, np.ndarray) and \
            not isinstance(angle_vec, tuple):
        raise ValueError("Sent angles not formatted in the correct way")
    # sending the angle to serial_port 
    send_string = angle_string_maker(angle_vec)
    try:
        serial_port.write(send_string)
    except:
        raise IOError('Unable to write string to serial port.')
    # wait a little for the arduino to send stuff back
    time.sleep(WAIT_MILLIS/float(1000))
    return_angle = recv(serial_port)
    if validate(angle_vec, return_angle):
        return True
    else:
        return False 

def recv(serial_port, verbose=False, delimiter=','):
    """ Function to receive a string of comma separated angles
    args:
        serial_port: the serial port
        verbose: True if you'd like the received data to be printed. False by
                 default.
        delimiter: The delimter used to separate different angle values
    Returns:
        recv_angles: the list/tuple/array of serial_received
    """
    try:
        data_line = serial_port.readline()
    except:
        raise IOError('Unable to read line from the serial port')
    # parsing the data_line
    try:
        data = angle_string_parser(data_line)
    except:
        raise ValueError('Unable to convert to list of angles.')
    if verbose:
        # get time
	t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        print('Received angles at {}: {}'.format(t, data_line))
    return data

def validate(sent_angles, recv_angles):
    """ Function to validate that the recv and angles match
    Args:
        sent_angles: list of angles sent
        recv_angles: list of angles received
    Returns:
        True if they match, false otherwise.
    """
    if not isinstance(sent_angles, list) and \
            not isinstance(sent_angles, np.ndarray) and \
            not isinstance(sent_angles, tuple):
        raise ValueError("Sent angles not formatted in the correct way")
    if not isinstance(recv_angles, list) and \
            not isinstance(recv_angles, np.ndarray) and \
            not isinstance(recv_angles, tuple):
        raise ValueError("received angles not formatted in the correct way")
    if isinstance(sent_angles, np.ndarray):
        # converting to list
        sent_angles = sent_angles.tolist()
    if isinstance(recv_angles, np.ndarray):
        # converting to list
        recv_angles = recv_angles.tolist()
    return recv_angles == sent_angles


