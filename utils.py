import cv2
import numpy as np
import re


def drawtext(framedata, coords, text="No data", ):
    """
    Draws the requested text on top of a video frame
    :param framedata:   the video frame
    :param coords:      X, Y coordinates of the left-bottom corner of a text rectangle
    :param text:        the text to be printed (default = "No data")
    """
    # select font type
    font = cv2.FONT_HERSHEY_PLAIN
    # put text to the video device
    cv2.putText(framedata, text, coords, font, 1.2, (0, 0, 0), 2, cv2.FILLED)


def moving_avg_window (lst, windowsize, newval):
    """
    Calculates a simple moving average of the list.
    Keeps the list at the size that does not exceed the provided value, by
    appending a new value and popping out a first (oldest) value.
    :param lst:         the list of values to average
    :param windowsize:  the maximal size of the list allowed
    :param newval:      he most current value to append to the list
    :return: an updated list and its mean value
    """
    if len(lst) == windowsize + 1:
        lst.pop(0)
    lst.append(newval)
    return lst, np.mean(lst)


def linear_DRC(img1):
    """
    Scales down the video data to 8-bit for visual representation
    using a linear dynamic range compression mechanism
    :param img1: the video frame matrix
    :return: the data compressed to 8-bit
    """
    data = np.array(img1, dtype='f')
    data = data - data.min()
    data = data / data.max()
    return 255 * data
