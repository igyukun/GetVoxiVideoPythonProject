#Getting the live video from VOXI using SENSIA USB3 extender board

##Requirements:
- opencv-python - 4.6.0.66
- matplotlib - 3.6.2
- numpy - 1.20.1

##Functionality
1. Opens USB3 camera with SENSIA extender (_produced video format is YUV 4:2:2_). 
2. Reads video frames in the infinite loop and displays it within the OpenCv GUI window. 
3. Plots histogram for a single frame upon frame pausing.
4. Processes keyboard inputs:
   1. **'Q'** or **'q'** or **'ESC'** - terminate the execution and close the video screen. The execution can also be terminated upon clicking the **|X|** button in the right top corner of the screen.
   2. **'C'** or **'c'** - capture the current frame and strore it in the current directory as a PNG image
   3. **'P'** or **'p'** - pause the video and plot the histogram, calculated for the current frame. _Pressing on any key will cancel the pause._
   4. **'O'** or **'o'** - toggle the OSD (on-screen text) on and off.
5. Displays some basic run-time information:
   1. Approximated frame rate
   2. Dynamic range in gray levels (DL)
   3. The _global_ mean signal.