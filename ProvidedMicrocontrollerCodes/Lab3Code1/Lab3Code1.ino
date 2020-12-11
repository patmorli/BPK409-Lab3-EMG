/*
 * This code measures an analog signal with a given sampling frequency
 * To increase resolution, it uses the SparkFun Qwiic 12 Bit ADC and its library. 
 * This helps to change the range to 0-2.048V 
 * and increase the resolution from 10 bit to 11 bit.
 * Created by Patrick Mayerhofer June 2020
 * Modified by Patrick Mayerhofer December 2020 (added ADC)
 */


 
#include <SparkFun_ADS1015_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_ADS1015
#include <Wire.h>

ADS1015 adcSensor;

#define sf 1000 //change this for wanted sampling fq
#define tc (1000/(sf))     // time constant
unsigned int ADC_Value = 0;    //ADC current value
unsigned long last_time = 0;

void setup() {
  Wire.begin();
  Serial.begin(500000);
  if (adcSensor.begin() == true)
  {
    Serial.println("Device found. I2C connections are good.");
  }
  else
  {
    Serial.println("Device not found. Check wiring.");
    while (1); // stall out forever
  }
}


// the loop routine runs over and over again forever:
void loop() {
  ADC_Value = adcSensor.getSingleEnded(0);
  if (millis() - last_time >= tc) {
    last_time = millis();
    
    
    Serial.print(ADC_Value);
    Serial.print('\t');
    Serial.print(millis());
    Serial.println();
    }
}
