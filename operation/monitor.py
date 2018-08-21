"""
@author: Ian Huang
This script is for monitoring the states of each of the joints, and writing
them to file. This allows the old states to be recorded, and allows new
programs run on the robot to transition from the old state more naturally.
"""

import serial
import argparse
import os

FLAGS = None 

def write_last_state(data, save_loc='last_state.txt'):
    """
    Writes given data to the save_loc
    """
    with open(save_loc, 'w') as f:
        f.write(data)

def read_last_state(save_loc='last_state.txt'):
    """
    Reads last state from the save_loc
    """
    with open(save_loc, 'r') as f:
        n = f.readline()
    return n

def receive_port(port):
    data = port.readline()
    data.strip()
    return data

def send_port(port, data):
    port.write(str(data))

def print_port(port, save_loc, limit=None):
    if limit is None:
        while True:
            data = receive_port(port)
            print(data)
            write_last_state(data)
    else:
        assert isinstance(limit, int), 'limit must be an integer'
        assert limit > 0, 'limit must be positive'
        for i in range(limit):
            data = receive_port(port)
            print(data)
            write_last_state(data, save_loc=save_loc)

def send_previous_state(port):
    previous_state = str(read_last_state(FLAGS.state_loc)) 
    port.write(previous_state)
    return previous_state

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--state_loc',
        type=str,
        default='last_state.txt',
        help='path to the file recording the last state of the robot'
    )
    parser.add_argument(
        '--protocol',
        type=str,
        default='standby',
        help='The purpose of this monitor use.'
    )
    FLAGS, unparsed = parser.parse_known_args()
    port = serial.Serial('/dev/ttyACM0', 9600)
    if FLAGS.protocol.lower() == 'standby':
        prev_state = send_previous_state(port)
        print('collected and sent old state: {}'.format(prev_state))
        print_port(port, save_loc=FLAGS.state_loc, limit=100)
        port.close()
    if FLAGS.protocol.lower() == 'play':
        try:
            print_port(port, save_loc=FLAGS.state_loc, limit=None) 
        except KeyboardInterrupt:
            print('print_port stopped, will close port now.')
            port.close()


         
