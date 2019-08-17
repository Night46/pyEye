#!/usr/local/bin/python

import cv2 as cv
import numpy as np
import dlib
from math import hypot

import config
import out

class BlinkDetector(object):
    def __init__(self):
        self.capture = cv.VideoCapture(config.VIDEO_SOURCE)
        self.faceDetector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def center(self, position_1, position_2):
        return int((position_1.x + position_2.x)/2), int((position_1.y + position_2.y)/2)
    
    def grayScale(self, frame):
        convertedGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return convertedGray

    def detectFacePosition(self, videoOut):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    topLeft = face.left(), face.top()
                    bottomRight = face.right(), face.bottom()

                    print('pace position top left at: {} and bottom right at {}'.format(topLeft, bottomRight))
                    print('')

                    if videoOut == True:
                        self.faceVideoOutput(frame, topLeft, bottomRight)
    
    def calculateEyeBlinkRatio(self, positionLeft, positionRight, positionTopCenter, PositionBottomCenter):
        verticalLength = hypot((positionTopCenter[0] - PositionBottomCenter[0]), (positionTopCenter[1] - PositionBottomCenter[1]))
        horizentalLength = hypot((positionLeft[0] - positionRight[0]), (positionLeft[1] - positionRight[1]))

        return (horizentalLength / verticalLength)
    
    def detectRightEyeBlink(self, videoOut, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)
                    eyeLeft = (landmarks.part(36).x, landmarks.part(36).y)
                    eyeRight = (landmarks.part(39).x, landmarks.part(39).y)

                    eyeTopLeft = (landmarks.part(37).x, landmarks.part(37).y)
                    eyeTopRight = (landmarks.part(38).x, landmarks.part(38).y)
                    eyeTopCenter = self.center(landmarks.part(37), landmarks.part(38))

                    eyeBottomLeft = (landmarks.part(41).x, landmarks.part(41).y)
                    eyeBottomRight = (landmarks.part(40).x, landmarks.part(40).y)
                    eyeBottomCenter = self.center(landmarks.part(41), landmarks.part(40))

                    blinkValue = self.calculateEyeBlinkRatio(eyeLeft, eyeRight, eyeTopCenter, eyeBottomCenter)

                    if comOut != False and comOut in range(1, 5):
                        out.OutputToSerial.manageOut(comOut, blinkValue)
                    else:
                        print('top left distance from buttom left is {}'.format(eyeBottomLeft[1] - eyeTopLeft[1]))
                        print('top right distance from buttom right is {}'.format(eyeBottomRight[1] - eyeTopRight[1]))
                        print('')
                        print('top center position is {}'.format(eyeTopCenter))
                        print('bottom center position is {}'.format(eyeBottomCenter))
                        print('')
                        print('horizontal line DEVIDED by vertical line is {}'.format(blinkValue))
                    
                    if videoOut == True:
                        self.blinkVideoOutput(frame, eyeLeft, eyeRight, eyeTopRight, eyeTopLeft, eyeBottomRight, eyeBottomLeft, eyeTopCenter, eyeBottomCenter, blinkValue)
    
    def detectLeftEyeBlink(self, videoOut, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)
                    eyeLeft = (landmarks.part(42).x, landmarks.part(42).y)
                    eyeRight = (landmarks.part(45).x, landmarks.part(45).y)

                    eyeTopLeft = (landmarks.part(43).x, landmarks.part(43).y)
                    eyeTopRight = (landmarks.part(44).x, landmarks.part(44).y)
                    eyeTopCenter = self.center(landmarks.part(43), landmarks.part(44))

                    eyeBottomLeft = (landmarks.part(47).x, landmarks.part(47).y)
                    eyeBottomRight = (landmarks.part(46).x, landmarks.part(46).y)
                    eyeBottomCenter = self.center(landmarks.part(47), landmarks.part(46))

                    blinkValue = self.calculateEyeBlinkRatio(eyeLeft, eyeRight, eyeTopCenter, eyeBottomCenter)

                    if comOut != False and comOut in range(1, 5):
                        out.OutputToSerial.manageOut(comOut, blinkValue)
                    else:
                        print('top left distance from buttom left is {}'.format(eyeBottomLeft[1] - eyeTopLeft[1]))
                        print('top right distance from buttom right is {}'.format(eyeBottomRight[1] - eyeTopRight[1]))
                        print('')
                        print('top center position is {}'.format(eyeTopCenter))
                        print('bottom center position is {}'.format(eyeBottomCenter))
                        print('')
                        print('horizontal line DEVIDED by vertical line is {}'.format(blinkValue))
                    
                    if videoOut == True:
                        self.blinkVideoOutput(frame, eyeLeft, eyeRight, eyeTopRight, eyeTopLeft, eyeBottomRight, eyeBottomLeft, eyeTopCenter, eyeBottomCenter, blinkValue)
    
    def detectTwoEyeBlink(self, rightPositionsList=[36, 37, 38, 39, 40, 41], leftPositionsList=[42, 43, 44, 45, 46, 47], videoOut=False, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)
                    for position in [rightPositionsList, leftPositionsList]:
                        # positions list layout is clockwise as in:
                        # https://2.bp.blogspot.com/-MDiMLZ30HAc/WadbmA8MGsI/AAAAAAAADc8/xThyrD0pH08pTM1R9g6xJ-kCBsc-afE7ACLcBGAs/s1600/dlib-landmark-mean.png
                        eyeLeft = (landmarks.part(position[0]).x, landmarks.part(position[0]).y)
                        eyeRight = (landmarks.part(position[3]).x, landmarks.part(position[3]).y)

                        eyeTopLeft = (landmarks.part(position[1]).x, landmarks.part(position[1]).y)
                        eyeTopRight = (landmarks.part(position[2]).x, landmarks.part(position[2]).y)
                        eyeTopCenter = self.center(landmarks.part(position[1]), landmarks.part(position[2]))

                        eyeBottomLeft = (landmarks.part(position[5]).x, landmarks.part(position[5]).y)
                        eyeBottomRight = (landmarks.part(position[4]).x, landmarks.part(position[4]).y)
                        eyeBottomCenter = self.center(landmarks.part(position[5]), landmarks.part(position[4]))

                        leftEye = self.calculateEyeBlinkRatio(eyeLeft, eyeRight, eyeTopCenter, eyeBottomCenter)
                        rightEye = self.calculateEyeBlinkRatio(eyeLeft, eyeRight, eyeTopCenter, eyeBottomCenter)

                        twoEyeBlinkRatio = (leftEye + rightEye) / 2                        

                        if comOut != False and comOut in range(1, 5):
                            out.OutputToSerial.manageOut(comOut, twoEyeBlinkRatio)
                        else:
                            # TODO - add video output
                            print(twoEyeBlinkRatio)

    def faceVideoOutput(self, source, positonTopLeft, positonBottomRight):
        cv.rectangle(source, positonTopLeft, positonBottomRight, (0, 255, 0), 1)
        cv.imshow('FaceDetection', source)
        if cv.waitKey(1) & 0xFF == ord('q'):
            quit()

    def blinkVideoOutput(self, source, positionLeft, positionRight, positonTopRight, positonTopLeft, positonBottomRight, positonBottomLeft, topCenter, bottomCenter, eyeRation):
        cv.circle(source, positonTopLeft, 3, (0, 255, 0), 1)
        cv.circle(source, positonTopRight, 3, (0, 255, 0), 1)
        cv.circle(source, positonBottomLeft, 3, (0, 0, 255), 1)
        cv.circle(source, positonBottomRight, 3, (0, 0, 255), 1)
        cv.line(source, topCenter, bottomCenter, (0, 255, 0), 1)
        cv.line(source, positionLeft, positionRight, (0, 255, 0), 1)
        if eyeRation > config.CLOSED_EYE_RATIO:
            cv.putText(source, 'Eye is closed', (50, 150), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        cv.imshow('BlinkDetection', source)
        if cv.waitKey(1) & 0xFF == ord('q'):
            quit()

    def closeSession(self):
        self.capture.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    BLINK_DETECTOR = BlinkDetector()
    #
    # To redirect output to a serial port add a selected com ID from 1 - 4
    # e.g BLINK_DETECTOR.detectFacePosition(True, 1)
    #
    # BLINK_DETECTOR.detectFacePosition(True)
    # BLINK_DETECTOR.detectLeftEyeBlink(True)
    # BLINK_DETECTOR.detectRightEyeBlink(True)
    # BLINK_DETECTOR.detectTwoEyeBlink([36, 37, 38, 39, 40, 41], [42, 43, 44, 45, 46, 47])
