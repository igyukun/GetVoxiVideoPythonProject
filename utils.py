import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt


def drawtext(framedata, coords, text="No data", ):
    """
    Draws the requested text on top of a video frame
    :param framedata:   the video frame
    :param coords:      X, Y coordinates of the left-bottom corner of a text rectangle
    :param text:        the text to be printed (default = "No data")
    :return:            none
    """
    # select font type
    font = cv2.FONT_HERSHEY_SIMPLEX

    # put thin black text on top of white thick text to get the text visible on any background

    cv2.putText(framedata, text, coords, font, 0.4, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(framedata, text, coords, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)


def draw_stats(gray, fps, min_val, max_val, mean_val):
    """
    Draws video stats as a text on top of the video frame
    :param gray:        video array compressed by DRC
    :param fps:         video frame rate
    :param min_val:     video array minimum
    :param max_val:     video array maximum
    :param mean_val:    video array mean
    :return:            none
    """
    drawtext(gray, (10, 400), str(f"Frame rate: {fps} fps"))
    drawtext(gray, (10, 430), str(f"min: {min_val} DL <-> max: {max_val} DL."))
    drawtext(gray, (10, 460), str(f"Frame mean: {mean_val} DL."))
    drawtext(gray, (10, 20), "'Q/q' - terminate")
    drawtext(gray, (10, 50), "'C/c' - capture frame")
    drawtext(gray, (10, 80), "'P/p' - pause and plot")
    drawtext(gray, (10, 110), "'O/o' - toggle OSD")
    drawtext(gray, (10, 140), "'D/d' - toggle DRC")
    drawtext(gray, (10, 170), "'N/n' - Execute 1-Point NUC")

def drawErr (gray, errorMsg):
    drawtext(gray, (500, 200), errorMsg)

def draw_histogram(img, minval, maxval):
    """
    Draws the signal frequencies histogram calculated from the 14-bit image data
    :param img:     data matrix
    :param minval:  minimal value (to define the low limit of the data range)
    :param maxval:  maximal value (to define the high limit of the the data range)
    :return:        none
    """
    plt.hist(img.reshape(-1), density=True, bins=1000, range=(minval - 50, maxval + 50),
             color='green', histtype='stepfilled')
    plt.title("VOXI USB video")
    plt.xlabel('Value')
    plt.ylabel('Occurrences')
    plt.grid(color='red', linestyle='--', linewidth=0.5)
    plt.show()


def moving_avg_window(lst, windowsize, newval):
    """
    Calculates a simple moving average of the list.
    Keeps the list at the size that does not exceed the provided value, by
    appending a new value and popping out a first (oldest) value.
    :param lst:         the list of values to average
    :param windowsize:  the maximal size of the list allowed
    :param newval:      he most current value to append to the list
    :return:            an updated list and its mean value
    """
    if len(lst) == windowsize + 1:
        lst.pop(0)
    lst.append(newval)
    return lst, np.mean(lst)


def linear_drc(img1):
    """
    Scales down the video data to 8-bit for visual representation
    using a linear dynamic range compression mechanism
    :param img1:    the video frame matrix
    :return:        the data compressed to 8-bit
    """
    data = np.array(img1, dtype='f')
    data = data - data.min()
    data = data / data.max()
    return 255 * data
