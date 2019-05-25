"""
This module provides functionality for facial recognition.

Acknowledgement
This code is adapted from:
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
"""

import argparse
import pickle
import time
import imutils
from imutils.video import VideoStream
import cv2
import face_recognition


class FacialRecognition:
    """
    The FacialRecognition class provides functions of matching face with encodings.pickle
    encoding.pickles stored features of different images of faces whic stored in dataset
    All images were captured and encoded in advance

    Attributes:
        __username (str, None): username stored in encodings.pickle
        __args (dict, None): stores the arguments used for recognition
        __face_data: pre-encoded facial data
        __found (bool): predicates whether a matched face is found
        __video (VideoStream): a VideoStream instance
    """

    def __init__(self):
        self.__username = None
        self.__args = None
        self.__face_data = None
        self.__found = False
        self.__video = VideoStream()

    def __start_camera(self):
        """Starts the camera and loads the necessary data

        Returns:
            None

        """
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument("-e", "--encodings", default='encodings.pickle')
        argument_parser.add_argument("-r", "--resolution", type=int, default=240)
        argument_parser.add_argument("-o", "--output", type=str)
        argument_parser.add_argument("-y", "--display", type=int, default=0)
        argument_parser.add_argument("-d", "--detection-method", type=str, default="hog")
        self.__args = vars(argument_parser.parse_args())

        # Load the known faces and embeddings
        print("[INFO] loading encodings...")
        self.__face_data = pickle.loads(open(self.__args["encodings"], "rb").read())

        # initialize the video stream and pointer to output video file, then
        # allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        self.__video.start()
        time.sleep(2.0)

    def __scan_frame(self):
        """Scans one frame of the video feed to find matching user

        Returns:
            None

        """
        print('Scanning...')
        print('Please face the camera.')
        # grab the frame from the threaded video stream
        frame = self.__video.read()

        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = imutils.resize(frame, width=self.__args["resolution"])

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb,
                                                model=self.__args["detection_method"])
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.__face_data["encodings"],
                                                     encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matched_indexes = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for index in matched_indexes:
                    name = self.__face_data["names"][index]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

        if len(names) != 1:
            # If more than faces or no face were recognized, we count it as
            # not found, as only one user is allowed at a time
            self.__found = False
            print('Cannot recognize the face. Retrying...')
            # Set a flag to sleep the cam for fixed time
            time.sleep(2.0)
        else:
            # print to console, identified person
            print('Person found: {}'.format(name))
            self.__username = name
            self.__found = True

    def recognize(self):
        """Recognize the face to find username

        It will loop over video frame to look for matched faces.
        If nothing mathces, it will attempt again.

        Returns:
            None
        """
        while not self.__found:
            self.__scan_frame()

        # cleanup
        cv2.destroyAllWindows()
        self.__video.stop()

    def run(self):
        """Start the facial recognition process

        It starts the camera and recognizes the face

        Returns:
            str: username that matches the face
        """
        self.__start_camera()
        self.recognize()
        return self.__username
