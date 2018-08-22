#include <stdio.h>
#include <stdlib.h>
#include <Servo.h>
#include <assert.h>
#include "Time.h"

Servo myservo1;
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;
Servo myservo6;

bool newData = false;
int angles[6] = {0,0,0,0,0,0} ;

void comma_sep_parser(char *line){
    // Takes in a char*, converts char* to int, comma separated
    Serial.println("entering parser");
    const char *delim = ",";
    char *p = strtok(line, delim);
    int counter = 0;
    while (p != NULL){
        // convert *p to int, store into angles[counter]
        angles[counter] = atoi(p);
        // fetch next one
        p = strtok(NULL, delim);
        counter++;
    }
    assert(counter==6);
   
    Serial.println(angles[0]);
    Serial.println(angles[1]);
    Serial.println(angles[2]);
    Serial.println(angles[3]);
    Serial.println(angles[4]);
    Serial.println(angles[5]); 
}

void recv(){
    char buffer[30];
    byte ndx=0;
    char character;
    char endMarker = '\n';
    bool keepReading = true;
    while (Serial.available() && keepReading){
        Serial.println("reading");
        character = Serial.read();
        if (character != endMarker){
            buffer[ndx] = character;
            ndx++;
        }
        else{
            //null terminate the string
            buffer[ndx] = '\0';
            keepReading = false;
            newData = true;
        }
    }
    if (newData){
      Serial.println("Read %s from serial:");
      Serial.println(buffer);
      Serial.println("parsing");
      comma_sep_parser(buffer);
    }
 
    // pass string through parser, updating global variable
    newData = false;
}

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
    recv();
    // will send a confirmation of angles parsed
    Serial.print(angles[0]);
    Serial.print(", ");
    Serial.print(angles[1]);
    Serial.print(", ");
    Serial.print(angles[2]);
    Serial.print(", ");
    Serial.print(angles[3]);
    Serial.print(", ");
    Serial.print(angles[4]);
    Serial.print(", ");
    Serial.println(angles[5]);
    // TODO: waiting for validation for go ahead from raspberry pi
    // otherwise retry to recv.

    myservo1.write(angles[0]);
    myservo2.write(angles[1]);
    myservo3.write(angles[2]);
    myservo4.write(angles[3]);
    myservo5.write(angles[4]);
    myservo6.write(angles[5]);
   
    delay(1000);
}


