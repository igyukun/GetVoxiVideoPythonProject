# Read the video stream from VOxI camera
# through the USB3 interface
# and display the video with the frame rate
# min/max and mean value in the 14-bit range

import cv2
import numpy as np
import time
import utils as u

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0

# video statistics globals:
sFps = 0   # frame rate string
meanval = 0 # frame mean value
minval = 0  # frame minimum value
maxval = 0  # frame maximum value

# seconds counter to be used for refreshing the stats data on the screen
tic = time.time()
toc = time.time()
# defines the moving averaging window (number of frames)
avg_window = 1024
# the list of the individual frames durations with the length of up to 'avg_window'
frm_time_list = [0]

# Create a video capturing device instance
cam0 = cv2.VideoCapture(0)
# Convert the captured image to RGB
cam0.set(cv2.CAP_PROP_CONVERT_RGB, 0)

# Video presentation loop
# Iterate as long as a video capturing device is opened,
# the frame can be read or until 'Q' key is pressed
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

    # Calculate the fps and cast the result to int
    # the condition is set to prevent the division by '0' error
    if not new_frame_time == prev_frame_time:
        currfps = 1 / (new_frame_time - prev_frame_time)

    # Call utils.moving_avg_window function to filter down the frame rate fluctuations
    frm_time_list, meanfps = u.moving_avg_window(frm_time_list, avg_window, currfps)

    # assign the current time to the previous frame time
    prev_frame_time = new_frame_time

    # Scale down the video data from 16-bit to 14-bit format
    I = np.asarray(img0, dtype='>B').view(np.uint16) - 49152
    # Arrange the video frame data as two-dimensional array with 640 elements in a row
    img1 = np.reshape(I, (-1, 640))

    # Apply a linear DRC to scale the video down from 14-bit to 8-bit
    gray = u.linear_DRC(img1)

    # Update the video stats once in every second
    if (toc - tic) >= 1.0:
        sFps = int(meanfps)
        minval = np.min(img1)
        maxval = np.max(img1)
        meanval = round(np.mean(img1))
        # update the tic seconds counter
        tic = time.time()

    # Draw the video statistics on top of the video frame (frame rate, minimum, maximum and mean values)
    u.draw_stats(gray, sFps, minval, maxval, meanval)

    # Display compressed video data with the OSD text
    cv2.imshow('VOXI USB video', gray.astype('uint8'))

    # Exit the video displaying loop condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release and destroy video acquisition device instance
cam0.release()
cv2.destroyAllWindows()


