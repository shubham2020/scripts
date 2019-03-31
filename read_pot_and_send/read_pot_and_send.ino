int sensorPin = A0;
char dataString[50] = {0};
int sensorValue = 0;

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  sensorValue = analogRead(sensorPin);// a value increase every loop
  sprintf(dataString,"%02X",sensorValue); // convert a value to hexa 
  Serial.println(dataString);   // send the data
  //delay(1000);                  // give the loop some break
}
