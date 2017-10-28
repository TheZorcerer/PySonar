# Written by Zahran Sajid, A sonar system using an arduino sending data via serial to python using pygame which plots it on a display.
# Licensed under the terms of the  GNU GENERAL PUBLIC LICENSE V2, If you have not obtained a copy of it along with the program, Please write to:
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging as l   # IMPORTANT!
import time 
l.basicConfig(filename="log.txt", level=l.DEBUG)  # Initialize the logging.

l.debug("*******************************************************")  # All such statements with l.debug() is for debugging puposes, you can ignore them.
l.debug("Started PySonar on "+str(time.asctime(time.localtime(time.time())))+". Logging has started!")
print("PySonar by zahran")
l.debug("Initializing......")
print("Initializing.............")
l.debug("Importing all necessary modules")
import pygame as pg
import serial as s
from math import sqrt,sin
from os import chdir
import sys
import json
l.debug("Imports succesful!")

print ("Imports done...")
#DATA
all_serial = list()
sector1 = (27,171)      # These are the boundaries of all sectors
sector2 = (207,18)      # To recap, the program gets the ping length and the sector and accordingly plots it by,
sector3 = (436,29)      # Mapping the ping length to the no. pixels between the centre of the display and the boundary of that sector,
sector4 = (600,197)     # Then the line() function returns a list of all x,y coordinates between the boundary and the centre,
sector5 = (589,426)     # And based on that the program will selected the nth coordinate where n is the mapped ping length,
sector6 = (429,566)     # Which is blitted to the screen. Whoo! Thats it!
sector7 = (201,570)
sector8 = (26,416)
middle = (319,304)

dis_x = 624

dis_y = 596

all_stuff = [0,0,0,0,0,0]   # This list contains the latest coordinates which have been parsed.

port = "/dev/ttyACM0"    # Put whatever port the arduino has been connected to here

#END_DATA

print("Connecting to Arduino on port: ", port,"......")
l.debug("Now attempting to connect to arduino on port"+str(port))
try:
	arduino = s.Serial(port,115200)  # Connect to serial port...
except Exception as exception:
	print("Whoops! Looks like the arduino has not been connected! Please check and make sure the arduino has been connected on",port)
	l.debug("No arduino detected on "+ str(port) + ". Closing PySonar.")
	sys.exit(1)
l.debug("Connection succesful!")
print("Connected.")

def int_map(n):
	n = int(n)
	n = n/70*dis_x/2  # Pretty simple, it maps the ping length, to the no. of pixels such that 70 cm (can be adjusted, just change the new max ping length) = 624/2 pixels.
	return n

def parse_serial():
	stuff = arduino.read(20)  # Gets 20 bytes of serial data
	stuff = str(stuff)[2:]    # converts the byte form into a str, gets rid of the b'
	stuff = stuff[:-1]        # and the ' in the end.
	all_serial = all_serial.append(stuff) # Just for the raw log of all input
	stuff = stuff.split("*")  # splits it into seperate pieces, the transfer protocol is like *ping|sector*ping|sector* , so this makes it into a list of ping|sector
	kk = 0
	try:
		while(kk<=len(stuff)):
			if(len(stuff[kk])<5):  # Basically what this thing does is that it checks for incomplete data, and then gets rid of it, the arduino is set to send data pellets exactly 5 chars long,
				del stuff[kk]      # 3 for the ping length, one for the | and one for the sector no.
				kk -= 1
			kk += 1
	except Exception:
		l.debug("Serial parsed, got: "+str(stuff))
		return(stuff)

def line(x0, y0, x1, y1):
        points_in_line = []     # Ok, I'll confess, this is not really my code, this def, I got it off the net, it takes two pairs of x,y coordinates and returns all coordinates between them.
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points_in_line.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points_in_line.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points_in_line.append((x, y))
        return points_in_line

def get_coords(ping,sector):
	length = int(int_map(ping))    # So the aim of this def is to get all the coordinates between the middle and the sector = int(sector)
	sector = int(sector)
	if(sector == 1):               # This part just gets the appropriate coordinates for the margin of each sector, blah, blah....
		sector = sector1
	elif(sector == 2):
		sector = sector2
	elif(sector == 3):
		sector = sector3
	elif(sector == 4):
		sector = sector4
	elif(sector == 5):
		sector = sector5
	a = line(middle[0],middle[1],sector[0],sector[1]) # gets all the coordinates between the middle and the end of that sector.
	if(len(a)<length):
		return a[len(a)-1]  # Nothing much, just checks if the no. of coordinates is less than the ping length, might be because of an error, this corrects it.
		l.debug("Strange, the ping is longer than the maximum no. of pixels....Well, ignoring it.")
	else:
		return a[length]

def main():  
	ds = pg.display.set_mode((dis_x,dis_y))  # Sets up the display.
	l.debug("Ok, set up diplay: "+ str(ds))
	pg.display.set_caption("Sonar System-180")  # The caption
	back = pg.image.load("sonar_main_2.jpg")    # Loads the background.
	dot = pg.image.load("sonar_dot.jpg")        # Loads the dots which plot the object positions
	ds.blit(back,(0,0))                         # Blits the backgroundAll Graphics and displays have been loaded and set up! PySonar is ready to rock and roll!
	print("All Graphics and displays have been loaded and set up! PySonar is ready to rock and roll!")
	l.debug("All Graphics and displays have been loaded and set up! PySonar is ready to rock and roll!")
	while True:                          # Ok, here we go! *cracks knuckles*
		a = parse_serial()               # Gets a list of the ping lengths + sector in ping|sector format
		l.debug("Got parsed serial, " + str(a))
		s = list()                       # Declare the list s
		for i in a:
			s.append(i.split("|"))       # Now we get a list in which each element is a list containing the ping length and the sector respectively.
		for i in range(len(s)):          # One by one start assigning the each ping len + sector to a x,y coordinate and then putting them in all_stuff
			a = s[i]
			b = get_coords(a[0],a[1])    # gets the coords
			sector = int(a[1])
			if(sector == 1):
				all_stuff[1] = a[0]      # all_stuff contains the latest parsed coords as done on line 126, this bit puts the coord in the right place in the list, like if sector one, then all_stuff[1]
			elif(sector == 2):
				all_stuff[2] = a[0]      # If sector 2, the all_stuff[2],
			elif(sector == 3):
				all_stuff[3] = a[0]      # And so on.....
			elif(sector == 4):
				all_stuff[4] = a[0]
			elif(sector == 5):
				all_stuff[5] = a[0]
		for i in range(len(all_stuff)):  # Now this bit takes the newly parsed and arranged coords in all_stuff and blits 'em
			if(all_stuff[i] == 0):       # If the value is 0, it means that the arduino didn't find any object, so we ignore it.
				pass
			else:
				a = all_stuff[i]        # And this is the part which you have been waiting for, ladies and gentlemen! The Blitting of The Dot! :P
				a = get_coords(a,i)
				l.debug("A dot has been blit on", str(a))
				ds.blit(dot,a)          # Right here <-----
		for event in pg.event.get():
			if(event.type == pg.QUIT):  # Exit on getting a pygame.EXIT event.....
				with open("raw_serial_out.txt","a") as rsl:
					json.dump(rsl)
				print("Closing.....")
				sys.exit(0)
			elif(event.type == pg.KEYDOWN):  # In case the screen is full of dots and you want to reset, just press c,(NOT C!)
				if(event.key == pg.K_c):
					l.debug("C has been pressed, clearing screen")
					ds.blit(back,(0,0))      # Resets the background, clears everything.
					for i in range(len(all_stuff)):
						all_stuff[i] = 0     # Resets all_stuff
					pg.display.update()
		pg.display.update()   # Refreshes the display, ESSENTIAL!!

if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		sys.exit(0)
	except Exception as exception:
		l.debug("An error has occured, we are extremely sorry, the full error is:" + exception)
		print("ERROR!: Refer to log.txt for more info :(")
		sys.exit(1)