# Read the video stream from VOxI camera
# through USB3 interface
# and display the video with the frame rate
# and min/max value in 14-bit range

import cv2
import numpy as np
import time

# $$$$ NEW ADDITION $$$$
# =======================
# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0
# =======================
# $$$$ END OF NEW ADDITION$$$$

# creating the videocapture object
# and reading from the live video camera
# Change it to video filename if reading from a live camera

# Create a video capturing device instance
# Comment for a video file
cam0 = cv2.VideoCapture(0)
# Uncomment for a video file and enter valid path
# cam0 = cv2.VideoCapture("c:/Work/CS/AVT/AVT_New/engine-mode-deadpix-video.mp4")

# Convert the captured image to RGB
cam0.set(cv2.CAP_PROP_CONVERT_RGB, 0)

# Video presentation infinite loop
# while cam0.isOpened():
while True:

    # Read video frame
    s, img0 = cam0.read()

    # $$$$ NEW ADDITION $$$$
    # =======================
    # break if could not read the frame (e.g. end of video or camera goes offline
    if not s:
        break

    # Uncomment for a video file
    #img0 = cv2.resize(img0, (640, 480))

    # font which will be esed to display FPS
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    # time when we finish processing for this frame
    new_frame_time = time.time()

    # Calculating the fps

    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    if not new_frame_time == prev_frame_time:
        fps = 1 / (new_frame_time - prev_frame_time)

    prev_frame_time = new_frame_time

    # converting the fps into integer
    fps = int(fps)

    # converting the fps to string so that we can display it on frame
    # by using putText function
    sFps = str(f"Frame rate: {fps} fps")
    # =======================
    # $$$$ END OF NEW ADDITION$$$$

    # Convert video frame from 16-bit to 14-bit format array
    # Comment for a video file
    I = np.asarray(img0, dtype='>B').view(np.uint16) - 49152
    img1 = np.reshape(img0, (-1, 640))

    # Scale down the video data to 8-bit for visual representation
    # using a linear dynamic range compression mechanism
    data = np.array(img1, dtype='f')
    data = data - data.min()
    data = data / data.max()
    gray = 255 * data

    # $$$$ NEW ADDITION $$$$
    # =======================
    # putting the FPS count on the frame
    cv2.putText(gray, sFps, (7, 70), font, 1, (100, 255, 0), 3, cv2.LINE_AA)
    # =======================
    # $$$$ END OF NEW ADDITION $$$$

    # Display compressed video data
    cv2.imshow('frame0', gray.astype('uint8'))

    # Print the minimum and the maximum pixel value - 14-bit value
    cv2.putText(gray, str(f"min: {img1.min()} <-> max: {img1.max()}"), (50, 70), font, 1, (100, 255, 0), 3, cv2.LINE_AA)

    # Exit the video displaying loop condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release and destroy video acquisition device instance
cam0.release()
cv2.destroyAllWindows()
