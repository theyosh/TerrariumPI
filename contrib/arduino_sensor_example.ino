#include <Wire.h>
#include <MHZ.h>
#include <SoftwareSerial.h>
/****************************
code for arduino pro mini.
It is an example code to be able to integrate any sensor to TerrariumPi using arduino and i2c protocol together with the type of sensor "Arduino Sensor".
The example code transforms 3 HC-SR04 sensors and one MHZ19C sensor to a block of bytes and sends them through i2c.
****************************/
/***************************
A0 =>     | MH_Z19_RX
A1 =>     | MH_Z19_TX
A2 =>     |
A3 =>     |
A4 => SDA |
A5 => SCL |
A6 =>     |
A7 =>     |
 0 => RX  |
 1 => TX  |
 2 =>     |
 3 =>     | trigPin Sonar 3
 4 =>     | echoPin Sonar 3
 5 =>     | trigPin Sonar 2
 6 =>     | echoPin Sonar 2
 7 =>     | trigPin Sonar 1
 8 =>     | echoPin Sonar 1
 9 =>     | LED
****************************/

#define SOUND_VELOCITY 0.034
#define SDA_PIN 27
#define SCL_PIN 28
#define I2C_ADDRESS 0x08
#define FLOAT 4
#define INT 4
#define SONAR_SENDOR FLOAT
#define MHZ_SENSOR (2*INT)
#define DATALENCH ((3*SONAR_SENDOR)+MHZ_SENSOR)


typedef struct sonar {
  const int trigPin;
  const int echoPin;
};

struct sonar sonar1 = {7, 8};
struct sonar sonar2 = {5, 6};
struct sonar sonar3 = {3, 4};

// pin for uart reading
#define MH_Z19_RX 14
#define MH_Z19_TX 15

MHZ co2(MH_Z19_RX, MH_Z19_TX, MHZ19C);

float d1 = 0,
      d2 = 0,
      d3 = 0,
      d4 = 0;
int ppm  = 0,
    temp = 0;
int cnt = 0;
byte data[DATALENCH];

float getSonarDistance(sonar sonarSensor, float soundVelocity);
byte toByte(int invalue);
byte toByte(float invalue);

void setup() {
  Serial.begin(115200);                         // Starts the serial communication
  Serial.println();
  Serial.println("Starting");

  pinMode(sonar1.trigPin, OUTPUT);              // Sets the trigPin as an Output
  pinMode(sonar1.echoPin, INPUT);               // Sets the echoPin as an Input
  digitalWrite(sonar1.trigPin, LOW);
  pinMode(sonar2.trigPin, OUTPUT);              // Sets the trigPin as an Output
  pinMode(sonar2.echoPin, INPUT);               // Sets the echoPin as an Input
  digitalWrite(sonar2.trigPin, LOW);
  pinMode(sonar3.trigPin, OUTPUT);              // Sets the trigPin as an Output
  pinMode(sonar3.echoPin, INPUT);               // Sets the echoPin as an Input
  digitalWrite(sonar3.trigPin, LOW);

  Wire.begin(I2C_ADDRESS);                      // join i2c bus with address #8
  Wire.onRequest(RequestEvent);                 // register event

  Serial.println("Whait a evnet");
}

void loop() {
  d1 = getSonarDistance(sonar1,SOUND_VELOCITY);
  data[0] = ((byte*)&d1)[3];
  data[1] = ((byte*)&d1)[2];
  data[2] = ((byte*)&d1)[1];
  data[3] = ((byte*)&d1)[0];

  d2 = getSonarDistance(sonar2,SOUND_VELOCITY);
  data[4] = ((byte*)&d2)[3];
  data[5] = ((byte*)&d2)[2];
  data[6] = ((byte*)&d2)[1];
  data[7] = ((byte*)&d2)[0];

  d3 = getSonarDistance(sonar3,SOUND_VELOCITY);
  data[8] = ((byte*)&d3)[3];
  data[9] = ((byte*)&d3)[2];
  data[10] = ((byte*)&d3)[1];
  data[11] = ((byte*)&d3)[0];

  if(cnt <= 5){
    cnt++;
  }else{
    if (co2.isPreHeating()){
      ppm = co2.readCO2UART();
      temp = co2.getLastTemperature();
      cnt = 0;
      data[16] = ((byte*)&ppm)[3];
      data[17] = ((byte*)&ppm)[2];
      data[18] = ((byte*)&ppm)[1];
      data[19] = ((byte*)&ppm)[0];
      data[20] = ((byte*)&temp)[3];
      data[21] = ((byte*)&temp)[2];
      data[22] = ((byte*)&temp)[1];
      data[23] = ((byte*)&temp)[0];
    }
  }

  delay(1000);
}

void RequestEvent() {
  Wire.write(data,DATALENCH); //send data

  Serial.print("Distance S1 (cm): ");
  Serial.println(d1);
  Serial.print("Distance S2 (cm): ");
  Serial.println(d2);
  Serial.print("Distance S3 (cm): ");
  Serial.println(d3);
  Serial.print("PPM S4: ");
  Serial.println(ppm);
  Serial.print("Temperature S4: ");
  Serial.println(temp);
  for (int i=0; i<DATALENCH;i++){
    Serial.print(data[i],HEX);
    if((i+1)%4==0){
      Serial.print(" | ");
    }else{
      Serial.print(" ");
    }
  }
  Serial.println();
  Serial.println(DATALENCH);
  Serial.println("-------------------------------------------------------");

}

float getSonarDistance(sonar sonarSensor, float soundVelocity){
  // Clears the trigPin
  digitalWrite(sonarSensor.trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(sonarSensor.trigPin, HIGH);
  delayMicroseconds(100);
  digitalWrite(sonarSensor.trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(sonarSensor.echoPin, HIGH);

  // Calculate the distance
  return (duration * soundVelocity / 2);
}
