    # Read and display the video stream from VOxI camera using the USB3 interface in Y

import calendar
import cv2
import numpy as np
import time
from utils import *


# The time of the last and the current frames
prev_frame_time = 0
new_frame_time  = 0

# video statistics globals:
sFps    = 0   # frame rate string
meanval = 0 # frame mean value
minval  = 0  # frame minimum value
maxval  = 0  # frame maximum value
curfps  = 0
# seconds counter to be used for refreshing the stats data on the screen
tic = time.time()
toc = time.time()
# defines the moving averaging window (number of frames)
avg_window = 400
# the list of the individual frames durations with the length of up to 'avg_window'
frm_time_list = [0]
# OSD toggler
toggleOSD = True

# Create a video capturing device instance
cam0 = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Convert the captured image to RGB
cam0.set(cv2.CAP_PROP_CONVERT_RGB, 0)

s, img0 = cam0.read()

# Video presentation loop:
# Terminates when video capturing device is closed, the frame cannot be read or 'Q/q' key is pressed
while cam0.isOpened():

    # get the current time
    toc = time.time()
    # Read a new video frame
    s, img0 = cam0.read()
    # break if could not read the frame (e.g. end of video or camera goes offline
    if not s:
        break
    # time when we finished the current frame acquisition
    new_frame_time = time.time()

    # Calculate the fps and round the result to the closest integer
    # the condition is set to prevent the division by '0' error
    if not new_frame_time == prev_frame_time:
        currfps = round(1 / (new_frame_time - prev_frame_time))

    # Call utils.moving_avg_window function to filter down the frame rate fluctuations
    # frm_time_list, meanfps = moving_avg_window(frm_time_list, avg_window, currfps)
    frm_time_list, meanfps = moving_avg_window(frm_time_list, avg_window, currfps)
    # assign the current time to the previous frame time
    prev_frame_time = new_frame_time

    # Scale down the video data from 16-bit to 14-bit format
    I = np.asarray(img0).view(np.uint16) - 49152
    # No need to convert the data type with the use of DSHOW video capturing
    # I = np.asarray(img0, dtype='>B').view(np.uint16) - 49152

    # Arrange the video frame data as two-dimensional array with 640 elements in a row
    img1 = np.reshape(I, (-1, 640))

    # Apply a linear DRC to scale the video down from 14-bit to 8-bit
    gray = linear_DRC(img1)

    # Update the video stats once a second
    if (toc - tic) >= 1.0:
        sFps = int(meanfps)
        minval = np.min(img1)
        maxval = np.max(img1)
        meanval = round(np.mean(img1))
        # update the tic seconds counter
        tic = time.time()

    # Draw the video statistics on top of the video frame (frame rate, minimum, maximum and mean values)
    if toggleOSD:
        draw_stats(gray, sFps, minval, maxval, meanval)

    # Display compressed video data with the OSD text
    cv2.namedWindow("VOXI USB video", cv2.WINDOW_NORMAL)
    cv2.imshow('VOXI USB video', gray.astype('uint8'))

    # Process the keypress events
    key = cv2.pollKey()
    # terminate application
    if key == ord('q') or key == ord('Q') or cv2.getWindowProperty('VOXI USB video',cv2.WND_PROP_VISIBLE) == 0:
        break
    # capture the current frame into a file
    if key == ord('c') or key == ord('C'):
        cv2.imwrite(f'Capture_{calendar.timegm(time.gmtime())}.png', gray)
    # pause the video and plot the current frame histogram
    if key == ord('p') or key == ord('P'):
        draw_histogram(img1, minval, maxval)
        # pause until the next keypress
        cv2.waitKey(0)
    # press 'o' key to toggle the OSD on and off
    if key == ord('o') or key == ord('O'):
        if toggleOSD:
            toggleOSD = False
        else:
            toggleOSD = True

# release and destroy video acquisition device instance
cam0.release()
cv2.destroyAllWindows()


