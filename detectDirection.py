#!/usr/local/bin/python

import cv2 as cv
import numpy as np
import dlib
from math import hypot

import config
import out


class DirectionDetector(object):
    def __init__(self):
        self.capture = cv.VideoCapture(config.VIDEO_SOURCE)
        self.faceDetector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            'shape_predictor_68_face_landmarks.dat')

    def minMax(self, positionsList):
        min_x = np.min(positionsList[:, 0])
        max_x = np.max(positionsList[:, 0])
        min_y = np.min(positionsList[:, 1])
        max_y = np.max(positionsList[:, 1])

        return [min_x, max_x, min_y, max_y]

    def grayScale(self, frame):
        convertedGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return convertedGray

    def getRatio(self, positionsList, eyeLandmarks, frame):
        eyeRegion = np.array([(eyeLandmarks.part(positionsList[0]).x, eyeLandmarks.part(positionsList[0]).y),
                              (eyeLandmarks.part(positionsList[1]).x, eyeLandmarks.part(positionsList[1]).y),
                              (eyeLandmarks.part(positionsList[2]).x, eyeLandmarks.part(positionsList[2]).y),
                              (eyeLandmarks.part(positionsList[3]).x, eyeLandmarks.part(positionsList[3]).y),
                              (eyeLandmarks.part(positionsList[4]).x, eyeLandmarks.part(positionsList[4]).y),
                              (eyeLandmarks.part(positionsList[5]).x, eyeLandmarks.part(positionsList[5]).y), ], np.int32)

        ranges = self.minMax(eyeRegion)
        rightEye = frame[ranges[2]:ranges[3], ranges[0]:ranges[1]]
        graydOutRegion = cv.cvtColor(rightEye, cv.COLOR_BGR2GRAY)

        eyeThreshold = cv.adaptiveThreshold(graydOutRegion, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        thresholdView = cv.resize(eyeThreshold, None, fx=5, fy=5)

        height, width = eyeThreshold.shape
        leftSideThreshold = eyeThreshold[0: height, 0: int(width / 2)]
        leftSideWhite = cv.countNonZero(leftSideThreshold)

        rightSideThreshold = eyeThreshold[0: height, int(width / 2): width]
        rightSideWhite = cv.countNonZero(rightSideThreshold)

        directionRatio = leftSideWhite / rightSideWhite
        
        return (directionRatio)

    def rightEyedirection(self, videoOut, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)                   
                    directionRatio = self.getRatio([36, 37, 38, 39, 40, 41], landmarks, frame)

                    if comOut != False and comOut in range(1, 5):
                        out.OutputToSerial.manageOut(comOut, directionRatio)
                    else:
                        print(directionRatio)

                    if videoOut == True:
                        cv.putText(frame, str(directionRatio), (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        cv.imshow('Right Eye Direction', frame)
                        if cv.waitKey(1) & 0xFF == ord('q'):
                            quit()

    def leftEyedirection(self, videoOut, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)                   
                    directionRatio = self.getRatio([42, 43, 44, 45, 46, 47], landmarks, frame)

                    if comOut != False and comOut in range(1, 5):
                        out.OutputToSerial.manageOut(comOut, directionRatio)
                    else:
                        print(directionRatio)

                    if videoOut == True:
                        cv.putText(frame, str(directionRatio), (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        cv.imshow('Left Eye Direction', frame)
                        if cv.waitKey(1) & 0xFF == ord('q'):
                            quit()

    def twoEyesdirection(self, videoOut, comOut=0):
        while self.capture.isOpened():
            sucess, frame = self.capture.read()

            if sucess:
                gray = self.grayScale(frame)
                faceStream = self.faceDetector(gray)
                for face in faceStream:
                    landmarks = self.predictor(gray, face)
                    rightEyeRatio = self.getRatio([36, 37, 38, 39, 40, 41], landmarks, frame)
                    leftEyeRatio = self.getRatio([42, 43, 44, 45, 46, 47], landmarks, frame)
                    
                    directionRatio = (rightEyeRatio + leftEyeRatio) / 2

                    if comOut != False and comOut in range(1, 5):
                        out.OutputToSerial.manageOut(comOut, directionRatio)
                    else:
                        print(directionRatio)

                    if videoOut == True:
                        if directionRatio < config.LOOKING_RIGHT:
                            cv.putText(frame, 'Looking right' + str(directionRatio), (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        elif directionRatio > config.LOOKING_RIGHT and directionRatio < config.LOOKING_LEFT:
                            cv.putText(frame, 'Looking stright' + str(directionRatio), (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        elif directionRatio > config.LOOKING_LEFT:
                            cv.putText(frame, 'Looking left' + str(directionRatio), (50, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        
                        cv.imshow('Left Eye Direction', frame)
                        if cv.waitKey(1) & 0xFF == ord('q'):
                            quit()

if __name__ == '__main__':
    DIRECTION_DETECTOR = DirectionDetector()
    # 
    # To redirect output to a serial port add a selected com ID from 1 - 4
    # e.g DIRECTION_DETECTOR.rightEyedirection(True, 1)
    # 
    # DIRECTION_DETECTOR.rightEyedirection(True)
    # DIRECTION_DETECTOR.leftEyedirection(True)
    # DIRECTION_DETECTOR.twoEyesdirection(True)
