import sys
import serial
from serial.tools import list_ports

import config
import detectBlink
import detectDirection

class MainRun(object):
    def __init__(self):
        self.blink = detectBlink.BlinkDetector()
        self.direction = detectDirection.DirectionDetector()

        self.args = sys.argv
        self.argOptions = ['blink', 'direction']
        self.localPorts = list_ports.comports()
        self.localHelp ='''
expecting direction type and option:
[-] for type blink
    [-] chose eithr: facePosition / leftEye / rightEye / twoEyes
    [-] set the video output to either: True / False
    [-] set redirect to COM to 0 for disable, 1-4 for relative com port

        [-] e.g pythom main.py blink rightEye False 0

[-] for type direction
    [-] chose eithr: leftEye / rightEye / twoEyes
    [-] set the video output to either: True / False
    [-] set the redirect to COM port ID if needed, if enabled, make sure to edit the config file

        [-] e.g pythom main.py direction rightEye False 0
'''

    def getSerialComPoerts(self):
        localPorts = self.localPorts

        for port in localPorts:
            print('Following are the system available ports, set your selected port in the config.py file')
            print(port)

    def callDetection(self):
        if len(self.args) == 5:
            method = str(self.args[1])
            option = str(self.args[2])
            videoOut = self.args[3]
            comOut = self.args[4]
            
            if method in self.argOptions:
                if method == 'blink':
                    if option == 'rightEye':
                        self.blink.detectRightEyeBlink(videoOut, comOut)
                    elif option == 'leftEye':
                        self.blink.detectLeftEyeBlink(videoOut, comOut)
                    elif option == 'twoEyes':
                        self.blink.detectTwoEyeBlink(videoOut, comOut)
                elif method == 'direction':
                    if option == 'rightEye':
                        self.direction.rightEyedirection(videoOut, comOut)
                    elif option == 'leftEye':
                        self.direction.leftEyedirection(videoOut, comOut)
                    elif option == 'twoEyes':
                        self.direction.twoEyesdirection(videoOut, comOut)
            else:
                print('unsupported method')
        elif len(self.args) == 2:
            if self.args[1] == 'listCom':
                self.getSerialComPoerts()
            else:
                print('unsupported method')
        else:
            print(self.localHelp)

if __name__ == '__main__':
    MAIN_RUN = MainRun()
    # GET_COM_PORTS = MAIN_RUN.getSerialComPoerts()
    CALL_DETECTION = MAIN_RUN.callDetection()
