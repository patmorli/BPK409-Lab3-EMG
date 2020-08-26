
#define sf 1000 //change this for wanted sampling fq
//~ #define tc (1000/(sf))     // time constant
#define tc 1000
unsigned int ADC_Value = 0;    //ADC current value
unsigned long last_time = 0;
void setup() {
  Serial.begin(500000);
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
