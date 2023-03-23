import numpy as np
from matplotlib import pyplot as plt
from utils import *

# GAIN_FILE_PATH = r'c:/SCD/GainVOxI.bin'
GAIN_FILE_PATH = r'C:\Work\Voxi\Procedures\Gain tables\Gains_VX000586.bin'

def calc_diagonal(arr):
    diag_line = []
    move_step = 480/640
    for j in range(640):
        diag_line.append(arr[round(j*move_step)][j])
    return diag_line

dtype = np.dtype(np.uint16)
try:
    with open(GAIN_FILE_PATH) as f:
        data = np.fromfile(f, dtype)

    # arr = np.reshape(np.round(100 * data/(2**14)), (-1, 656))
    arr = np.reshape(data / (2 ** 14), (-1, 656))
    arr = np.delete(arr, np.s_[0 : 16], axis=1)
    plt.subplot(1,2,1)
    plt.imshow(arr, cmap='hot')
    # drc_arr = linear_drc(arr)
    # print(drc_arr)
    # plt.imshow(drc_arr, cmap='hot')
    plt.colorbar()
    # plt.show()

    plt.subplot(1,2,2)
    line1 = plt.plot(arr[5],'b-')
    line2 = plt.plot(arr[240],'r-')
    line3 = plt.plot(calc_diagonal(arr), 'g-')
    plt.legend(["row 5", "row 240", "diagonal (0,0)->(639,479)"], loc="best")
    plt.show()

except IOError as err:
    print(err.message)


