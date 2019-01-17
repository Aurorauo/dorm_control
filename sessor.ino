#include <OneWire.h>
#include <DS18B20.h>
// 1-Wire devices connected to digital pin 2 on the Arduino.
int temp=7;
DS18B20 ds(temp);
void setup() {
  pinMode(13,OUTPUT);  //测试
  Serial.begin(9600);
}

void loop()
{
    if(Serial.available() > 0) {
            char gain= Serial.read();
            if(gain=='a')
            {
              digitalWrite(13,LOW);
            }
            if(gain=='b')
            {
              digitalWrite(13,HIGH);
            }
            if(gain=='m')
            {
              boolean ledState=digitalRead(13);
              Serial.println(ledState);
              
            }
             if(gain=='t')//温度传感器
            {
                 // Tell every device to start a temperature conversion.
                ds.doConversion();
  
                 // Print alarm values and current temperature for every device with an active alarm condition.
 
                // Print current temperature to verify that it is still either < LOW_ALARM or > HIGH_ALARM.
                Serial.println(ds.getTempC());
            }

            
        }
    
}
