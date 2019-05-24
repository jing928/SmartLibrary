# USAGE
# With default parameter of user/id
#       python3 01_capture.py -n default_user
# OR specifying the dataset and user/id
#       python3 02_capture.py -i dataset -n default_user

## Acknowledgement
## This code is adapted from:
## https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

# import the necessary packages
# import the necessary packages
import cv2
import os
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
    help="The name/id of this person you are recording")
ap.add_argument("-i", "--dataset", default='dataset',
    help="path to input directory of faces + images")
args = vars(ap.parse_args())

# use name as folder name
name = args["name"]
folder = '../dataset/{}'.format(name)

# Create a new folder for the new name
if not os.path.exists(folder):
    os.makedirs(folder)

# Start the camera
cam = cv2.VideoCapture(0)
# Set video width
cam.set(3, 640)
# Set video height
cam.set(4, 480)
# Get the pre-built classifier that had been trained on 3 million faces
face_detector = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
# Create a window
#cv2.namedWindow("Saving Images... (Press Escape to end)")

img_counter = 0
while img_counter <= 10:
    key = input("Press q to quit or ENTER to continue: ")
    if key == 'q':
        break

    ret, frame = cam.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    if(len(faces) == 0):
        print("No face detected, please try again")
        continue

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        img_name = "{}/{:04}.jpg".format(folder,img_counter)
        cv2.imwrite(img_name, frame[y:y+h,x:x+w])
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
