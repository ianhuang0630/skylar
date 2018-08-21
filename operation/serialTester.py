import serial
import time

if __name__=='__main__':

    # connecting to the serial

    port = serial.Serial('/dev/ttyACM0', 9600)
    
    time.delay(100);
    print('hi')

    
