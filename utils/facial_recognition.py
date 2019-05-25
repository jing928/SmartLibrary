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
    """

    def __init__(self):
        self.__username = None

    def recognition(self):
        """Recognize the face to find username

        Returns:
            None

        """
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument("-e", "--encodings", default='encodings.pickle',
                                     help="path to serialized db of facial encodings")
        argument_parser.add_argument("-r", "--resolution", type=int, default=240,
                                     help="Resolution of the video feed")
        argument_parser.add_argument("-o", "--output", type=str,
                                     help="path to output video")
        argument_parser.add_argument("-y", "--display", type=int, default=0,
                                     help="whether or not to display output frame to screen")
        argument_parser.add_argument("-d", "--detection-method", type=str, default="hog",
                                     help="face detection model to use: either `hog` or `cnn`")
        args = vars(argument_parser.parse_args())

        # Load the known faces and embeddings
        print("[INFO] loading encodings...")
        data = pickle.loads(open(args["encodings"], "rb").read())

        # initialize the video stream and pointer to output video file, then
        # allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        video_stream = VideoStream(src=0).start()
        writer = None
        time.sleep(2.0)

        # loop over frames from the video file stream

        for _ in (0, 5):
            # grab the frame from the threaded video stream
            frame = video_stream.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = imutils.resize(frame, width=args["resolution"])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb,
                                                    model=args["detection_method"])
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
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
                        name = data["names"][index]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for ((_, _, _, _), name) in zip(boxes, names):
                # print to console, identified person
                print('Person found: {}'.format(name))

                # Set a flag to sleep the cam for fixed time
                time.sleep(3.0)
                self.__username = name
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.__video.stop()

    def recognize(self):
        """Get user name using facial recognition

        Returns:
            str: username that matches the face

        """
        self.recognition()
        return self.__username
