import cv2
import numpy as np

# Create a video capturing device instance
cam0 = cv2.VideoCapture(0)

# Convert the captured image to RGB
cam0.set(cv2.CAP_PROP_CONVERT_RGB, 0)

# Video presentation infinite loop
while (True):

    # Read video frame
    s, img0 = cam0.read()

    # Convert video frame from 16-bit to 14-bit format array
    I = np.asarray(img0, dtype='>B').view(np.uint16) - 49152
    img1 = np.reshape(I, (-1, 640))

    # Scale down the video data to 8-bit for visual representation
    # using a linear dynamic range compression mechanism
    data = np.array(img1, dtype='f')
    data = data - data.min()
    data = data / data.max()
    gray = 255 * data

    # Display compressed video data
    cv2.imshow('frame0', gray.astype('uint8'))

    # Print the minimum and the maximum pixel value - 14-bit value
    print('Min <--> Max')
    print(str(img1.min()) + ' <--> ' + str(img1.max()))

    # Exit the video displaying loop condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release and destroy video acquisition device instance
cam0.release()
cv2.destroyAllWindows()
