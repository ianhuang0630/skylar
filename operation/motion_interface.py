"""
@author: Ian Huang
Implementation of the class that gets target joint values and send transition
joint values ot the arduino.
"""
import time
import numpy as np
import tqdm

def AngleCommander(object):
    def __init__(self, temp_definition=0.25):
        self.old_state = None
        self.temp_definition = temp_definition

    def goTo(self, angle_vec, timespan = 1.0):
        """ method for sending the angles to the robot arm 
        Args:
            angle_vec (list): angle vector sent to the robot. The length of
                              the list is the number of joints in the robot.
            timespan (float): the number of seconds that the transition should
                              take.
        Return:
            True if angle was successfully sent, false otherwise.
        """
        if not isinstance(angle_vec, list):
            try: 
                angle_vec = angle_vec.tolist()
            except:
                try:
                    angle_vec = list(angle_vec)
                except:
                    raise ValueError('invalid input type')
        # getting the smoothing function
        smooth_f = self.getCubicSmoothing(self.old_state, angle_vec, timespan)
        # sending at regular intervals
        for i in range(np.ceil(timespan/float(self.temp_definition))):
            # one timestep
            send(smoothing_f(min(i*self.temp_definition, timespan)))
            # sleep for self.temp_definition
            time.sleep(self.temp_definition)
        # setting the oldstate to the new angle
        self.old_state = angle_vec
        # option of logging the new angle
        
    def getCubicSmoothing(self, theta1, theta2, tau):
        """ Calculates the coefficients for cubic theta(t). This assumes
            one would want the angular velocity graph to be concave quadratic.
        Args:
            theta1 (list): current joint angles
            theta2 (list): destination joint angles
            tau (float): time in seconds 
        Returns:
            a cubic function with the calculated coefficients
        """
        # calfculating coefficients -- derivations in the doc folder
        delt_Theta = np.array(theta2) - np.array(theta1)
        alpha = -2/(float(tau)**3) * delt_Theta
        beta = 3/(float(tau)**2) * delt_Theta
        integ_const = np.array(theta1)
        def f(t):
            assert isinstance(t, float), 'time must be a float'
            return alpha*(t**3) + beta*(t**2) + integ_const
        return f 

    def logState(self):
        pass
    def visualCapture(self):
        pass
