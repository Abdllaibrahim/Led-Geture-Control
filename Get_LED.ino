#include <cvzone.h>

SerialData serialData(1, 3); //(numOfValsRec,digitsPerValRec)
int valsRec[1]; // array of int with size numOfValsRec 

void setup() {
  pinMode(10, OUTPUT);
  serialData.begin();
 
}

void loop() {

  serialData.Get(valsRec);
  analogWrite(10, valsRec[0]);
 
  //delay(10);
  
}
