# PySonar

This is the code for a arduino based sonar system which grabs ping lengths in cm from the ultrasonic sensor,
sends it to a computer running the PySonar.py file on python3.5.

The program plots the data out by mapping the ping length to the no. pixels between the centre of the display and the boundary of that sector, ( The display is divided into 8 sectors). Then the line() function returns a list of all x,y coordinates between the boundary and the centre. Based on that the program will selected the nth coordinate where n is the mapped ping length, which is blitted to the screen. Whoo! 

This is the basics of how it works.

Hardware requirements are an Arduino, a USB cable, a servo with 180 degree rotation (minimum), a computer (obviously), an ultrasonic sensor.

For software requirements and how to run it, please refer to BUILDING.md.
Enjoy!!!
