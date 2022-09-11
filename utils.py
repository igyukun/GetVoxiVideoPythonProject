import cv2
import numpy as np

# This function draws the requested text on top of video frame.
# Args:
#   framedata   - the video frame
#   coords      - X, Y coordinates of the left-bottom corner of a text rectangle
#   text        - the text to be printed (default = "No data")
def drawtext(framedata, coords, text="No data", ):
    # select font type
    font = cv2.FONT_HERSHEY_PLAIN
    # put text to the video device
    cv2.putText(framedata, text, coords, font, 1.2, (0, 0, 0), 1, cv2.FILLED)

# This function maintains the list at the size not greater then the provided value.
# To do that, it appends a new value and pops out a first (oldest) value .
# Args:
#   lst         - the list of values to average
#   windowsize  - the maximal size of the list allowed
#   newval      - the most current value to append to the list
# Returns:
#   updated list and list mean value
def moving_avg_window (lst, windowsize, newval):
    if len(lst) == windowsize + 1:
        lst.pop(0)
    lst.append(newval)
    return lst, np.mean(lst)
