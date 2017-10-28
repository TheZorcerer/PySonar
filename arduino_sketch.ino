/*
* This is the accompanying arduino sketch to the PySonar python program.
* You will require an arduino board, an ultrasonic sensor (which I will hence forth refer to as the 'sonar'), a servo motor and a USB cable.
* The sonar must be connected so that the trigger pin is given to 2, the echo pin to 3.
* The servo must be given to pin 9.
*/


#include<NewPing.h>  // Include libraries.....
#include<Servo.h>
int distance = 0;   // Declare integers distance and rotation
int rotation = 0;
NewPing sonar(2,3,100);   // Trigger pin = 2, Echo pin = 3, max distance = 200. Make sure the sonar is connected like this.

Servo S;
void setup() {
  S.attach(9);      // Connect the servo to pin 9
  Serial.begin(115200);   // Initialize the serial communication.

}

void loop() {
  S.write(0);   // Start.
  delay(1000);  
  distance = sonar.ping_cm();  // Get the distance
  send_stuff(distance,1);      // Send it to the computer along with the sector, which is 1
  delay(25);                   //Same thing over and over again....
  S.write(45);
  delay(500);
  distance = sonar.ping_cm();
  send_stuff(distance,2);
  delay(25);
  S.write(45*2);
  delay(500);
  distance = sonar.ping_cm();
  send_stuff(distance,3);
  delay(25);
  S.write(45*3);
  delay(500);
  distance = sonar.ping_cm();
  send_stuff(distance,4);
  delay(25);
  S.write(45*4);
  delay(500);
 S.write(45*4);
  distance = sonar.ping_cm();
  send_stuff(distance,5);
  delay(500);
  delay(25);
  delay(25);

}

void send_stuff(int ping_length,int sector){   // This sends it to the computer via serial, and makes sure the entire message data is 5 characters long. Why? Refer to PySonar.py, line 59
  
  Serial.write("*");                   // Start with a *
  if(ping_length>99){
    Serial.print(ping_length);
  } else {
    if(ping_length>9){
    Serial.print("0");
    Serial.print(ping_length);
    } else {
      Serial.print("00");
      Serial.print(ping_length);
    }
  }
  Serial.write("|");
  Serial.print(sector);
  Serial.write("*");    // End also with a *
  

}


