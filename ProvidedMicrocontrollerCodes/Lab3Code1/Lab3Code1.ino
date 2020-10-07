/*
 * This code measures an analog signal with a given sampling frequency
 * 3.3V pin needs to be connected to AREF pin. We do this 
 * to increase the resolution by changing the analog input 
 * range from 0-5V to 0-3.3V.
 * Created by Patrick Mayerhofer June 2020
 */


#define sf 1000 //change this for wanted sampling fq
//~ #define tc (1000/(sf))     // time constant
#define tc 1000
unsigned int ADC_Value = 0;    //ADC current value
unsigned long last_time = 0;
void setup() {
  Serial.begin(500000);
  analogReference(EXTERNAL); // use AREF for reference voltage
}


// the loop routine runs over and over again forever:
void loop() {

  if (micros() - last_time >= tc) {
    last_time = micros();
    ADC_Value = analogRead(A0);
    
    Serial.print(ADC_Value);
    Serial.print(',');
    Serial.print(millis());
    Serial.println();
    }
}
