#include <OneWire.h>
#include <DS18B20.h>

int temp=7; //温度传感器所接引脚号
DS18B20 ds(temp);

void setup() {
  pinMode(13,OUTPUT);  //测试LED
  Serial.begin(9600);//设置波特率
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
            if(gain=='m')//获取LED引脚电平信号
            {
              boolean ledState=digitalRead(13);
              Serial.println(ledState);
              
            }
             if(gain=='t')//温度传感器
            {
                ds.doConversion();
                Serial.println(ds.getTempC());
            }

            
        }
    
}
