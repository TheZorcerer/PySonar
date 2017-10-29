Software requirements are python3.x (It was tested with 3.5 but conceivably any version of 3.x should work), 
the Arduino IDE (For building and uploading the arduino sketch),
the pygame and pyserial libraries for python3.
You need the NewPing library for compiling the arduino sketch.

To run, simply cd into the directory where you installed it, make sure the port given in line 43 of PySonar.py is the same as
the port to which you have connected the arduino to which the sketch has been burned (make sure the pins are connected appropriately).
Then, type python3 ./PySonar.py

Thank you, and have fun!!!
