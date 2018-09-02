"""
@author: Ian Huang
Implementation of the class that gets target joint values and send transition
joint values ot the arduino.
"""
import time
import numpy as np

# TODO: create global dict log_mode --> [names of important keys in dict]
LOGMODE = {'PosTrans': ['currentPosition', 'previousPosition'],
           'Image': ['imagePath', 'currentPosition'],
           'Video': ['videoPath', 'currentPosition', 'previousPosition']}

def AngleCommander(object):
    def __init__(self, visual_directory, log_filepath, temp_definition=0.25, 
                 max_tries=5, max_cap_wait=10, num_joints=6):
        self.num_joints = num_joints 
        self.old_state = self.get_initial_state() 
        self.temp_definition = temp_definition
        self.max_tries = max_tries
        self.directory = visual_directory 
        self.logpath = log_filepath
        self.image_num = 0
        
    def get_initial_state(self, initial_angle=90):
        return [initial_angle] * self.num_joints

    def checkAngleLimits(self, angle_vec):
        """ This checks that the input angles are possible
        Args:
            angle_vec: angle vector. First entry corresponds to the first 
                       joint angle, and so on.
        Raises:
            ValueError: when an angle does not conform to the known rules
        """
        if len(angle_vec) != self.num_joints:
            raise ValueError('Not right number of angles.')
        if not all([element <=180 and element>=0 for element in angle_vec]):
            raise ValueError('Some angles not in 0-180 range: {}'.\
                             format(angle_vec))
        # TODO: check for joint collisions
        pass

    def goTo(self, angle_vec, timespan=1.0):
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
        self.checkAngleLimits(angle_vec)
        # getting the smoothing function
        smooth_f = self.getCubicSmoothing(self.old_state, angle_vec, timespan)
        # sending at regular intervals
        for i in range(np.ceil(timespan/float(self.temp_definition))):
            # one timestep
            counter = 1
            while not send(smoothing_f(min(i*self.temp_definition, timespan)))\
                    and counter <= self.max_tries:
                counter += 1
            # sleep for self.temp_definition
            if counter > self.max_tries:
                return False
            time.sleep(self.temp_definition)
        # setting the oldstate to the new angle
        self.old_state = angle_vec
        # option of logging the new angle
        return True

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
    
    def writeLine(self, mode, data):
        """ Write line in the log
        Args:
            mode (str): 'PosTrans' if position transition, 'Image' if image,
                        'Video' if video
            data (dict): a dictionary containing the relevant numbers.
                         if mode=='PosTrans', dict should have key 'oldPosition'
                         if mode=='Image', dict should have key 'imagePath',
                         and 'currentPosition'
                         if mode=='Video', dict should have key 'videoPath',
                         'currentPosition' and 'previousPosition'
        Returns:
            String line (with new line character) to save to current log file.
        """
        # checks for mode and data
        if mode not in LOGMODE:
            raise ValueError('{} is not an acceptable mode.'.format(mode))
        for element in LOGMODE[mode]:
            if element not in data:
                raise ValueError('Required key {} does not exist in the dict'.\
                                 format(element))
        # depending on the type of information being logged, use different
        if mode == 'PosTrans':
            return self.writePosTransLine(data['currentPosition'],
                                          data['previousPosition'])
        elif mode == 'Image':
            return self.writeImageLine(data['imagePath'],
                                       data['currentPosition'])
        else:
            return self.writeVideoLine(data['videoPath'],
                                       data['currentPosition'],
                                       data['previousPosition'])

    def writePosTransLine(self, currentPosition, oldPosition):
        """ Returns a string for position transition.
        Args:
        """
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        return "{}: {} to {}\n".format(t,
                                       oldPosition, # old position
                                       currentPosition# new position
                                       )
    
    
    def writeImageLine(self, image_path, current_position):
        """ Writes image path, new position
        Args:
        """
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) 
        return "{}: {} for position {}\n".format(t, # time
                                                 image_path, # path to image
                                                 current_position # current position
                                                 )

    def writeVideoLine(self, video_path, current_position, previous_position):
        """ Writes video filepath, starting position, final position
        """
        t = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())  
        return "{}: {} for position transitions from {} to {}\n".\
                format(t, # time
                       video_path, # path to video
                       previous_position, # starting position
                       current_position # final position
                       )

    def logState(self, mode, data):
        """ Method for logging the states to the desired location
        """
        # check for existence of file
        
        if os.path.exists(self.log_filepath):
            # if path exists, append to file
            io_mode = 'a'
        else:
            # if path doesn't exist, create file and write to it
            io_mode = 'w'
        with open (self.log_filepath, io_mode) as f:
            f.write(self.writeLine(mode, data))

    def imageCapture(self, max_cap_wait=10):
        """ Uses the raspistill command to capture a picture, and waits till
            it is captured.
        """
        # capture image using raspistill
        file_path = os.path.join(self.directory, "im_{}.jpg".\
                                 format(self.image_num))
        if subprocess.call('raspistill -vf -hf -o {}'.format(file_path),
                           shell=True):
            raise IOError('Error capturing current image')
        self.image_num += 1   
        # record this using raspi_still, connect with the current self.old_state
        assert os.path.exists(file_path)

    def videoStart(self):
        pass
    def videoStop(self):
        pass
