#include <stdio.h>
#include <stdlib.h>
#include <Servo.h>
#include "Time.h"

Servo myservo1;
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;
Servo myservo6;

int angle1;
int angle2;
int angle3;
int angle4;
int angle5;
int angle6;

int angles[6];

void setup() {
  // put your setup code here, to run once:
  myservo1.attach(11);
  myservo2.attach(10);
  myservo3.attach(9);
  myservo4.attach(6);
  myservo5.attach(5);
  myservo6.attach(3);
  Serial.begin(9600);
}

void loop() {
  target = myservo1
    
// read the Serial input, allocate to each of the servos

  for (int i = 30 ; i < 120; i++){
    myservo1.write(i);
    myservo2.write(20);
    myservo3.write(i);
    myservo4.write(i);
    myservo5.write(i);
    myservo6.write(i);
    Serial.println(i);
    delay(25);
  }

  for (int i = 120; i>30; i--){
    myservo1.write(i);
    myservo2.write(20);
    myservo3.write(i);
    myservo4.write(i);
    myservo5.write(i);
    myservo6.write(i);
    Serial.println(i);
    delay(25);
  }
// send Serial output, joint angles positions.

}


void parser(char *line){
    // Takes in a char*, converts char* to int, comma separated
    const char *delim = ',';
    char *p = strtok(line, delim);
    int counter = 0;
    while (p != NULL){
        // convert *p to int, store into angles[counter]
        angles[counter] = atoi(p);
        // fetch next one
        p = strtok(NULL, delim);
        counter ++;
    }
    assert(counter==6);
}

