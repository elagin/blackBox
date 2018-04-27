//RTC By Makuna

// Connect VCC of the BMP085 sensor to 3.3V (NOT 5.0V!)
// EOC is not used, it signifies an end of conversion
// XCLR is a reset pin, also not used here

#include <Wire.h> // must be included here so that Arduino library object file references work
#include <RtcDS1307.h>
#include <Adafruit_BMP085.h>
#include "DHT.h"
#include <MsTimer2.h>

#define DHTPIN 4 // номер пина, к которому подсоединен датчик

// Раскомментируйте в соответствии с используемым датчиком
// Инициируем датчик
DHT dht(DHTPIN, DHT22);
//DHT dht(DHTPIN, DHT11);

//#include <OneWire.h>
//#include <DallasTemperature.h>
//https://github.com/adafruit/Adafruit_Sensor

#define countof(a) (sizeof(a) / sizeof(a[0]))

RtcDS1307<TwoWire> Rtc(Wire);
Adafruit_BMP085 bmp;

//#define ONE_WIRE_BUS 4 /* Digitalport Pin 2 definieren */
//OneWire ourWire(ONE_WIRE_BUS); /* Ini oneWire instance */
//DallasTemperature sensors(&ourWire);/* Dallas Temperature Library für Nutzung der oneWire Library vorbereiten */

//float temperature;
float pressTemperature;
int32_t pressure;
float altitude;
float humidity;

void setup ()
{
  Serial.begin(9600);
  bmp.begin();
  dht.begin();

  Serial.print("compiled: ");
  Serial.print(__DATE__);
  Serial.println(__TIME__);

  //--------RTC SETUP ------------
  // if you are using ESP-01 then uncomment the line below to reset the pins to
  // the available pins for SDA, SCL
  // Wire.begin(0, 2); // due to limited pins, use pin 0 and 2 for SDA, SCL

  Rtc.Begin();

  RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
  printData(compiled);
  Serial.println();

  if (!Rtc.IsDateTimeValid())
  {
    // Common Cuases:
    //    1) first time you ran and the device wasn't running yet
    //    2) the battery on the device is low or even missing

    Serial.println("RTC lost confidence in the DateTime!");

    // following line sets the RTC to the date & time this sketch was compiled
    // it will also reset the valid flag internally unless the Rtc device is
    // having an issue

    Rtc.SetDateTime(compiled);
  }

  if (!Rtc.GetIsRunning())
  {
    Serial.println("RTC was not actively running, starting now");
    Rtc.SetIsRunning(true);
  }

  RtcDateTime now = Rtc.GetDateTime();
  if (now < compiled)
  {
    Serial.println("RTC is older than compile time!  (Updating DateTime)");
    Rtc.SetDateTime(compiled);
  }
  else if (now > compiled)
  {
    Serial.println("RTC is newer than compile time. (this is expected)");
  }
  else if (now == compiled)
  {
    Serial.println("RTC is the same as compile time! (not expected but all is fine)");
  }

  // never assume the Rtc was last configured by you, so
  // just clear them to your needed state
  Rtc.SetSquareWavePin(DS1307SquareWaveOut_Low);

  Serial.println("pressure, pressTemperature, altitude, humidity");

  //flash();
  //MsTimer2::set(1000, flash);
  //MsTimer2::start();

  //MsTimer2::stop();

  //sensors.begin();/* Inizialisieren der Dallas Temperature library */

  //adresseAusgeben(); /* Adresse der Devices ausgeben */
}

int maxIter = 10;
int humidityRate = 6;
int temperatureRate = 2;
int iter = 0;

/*
  void flash()
  {
  MsTimer2::stop();

  Serial.println("FLASH");
  if (iter % humidityRate == 0)
  {
    //Console.Out.WriteLine("humidityRate");
    Serial.println("humidityRate");
    //getHumidity();
    //humidityRate = 0;
  }
  if (iter % temperatureRate == 0)
  {
    //Console.Out.WriteLine("temperatureRate");
    Serial.println("temperatureRate");
    //pressTemperature =  bmp.readTemperature();
    //temperatureRate = 0;
  }

  //getPressure();

  if (iter > maxIter)
  {
    //Console.Out.WriteLine("maxIter");
    Serial.println("maxIter");
    iter = 0;
    //return;
  }
  else
  {
    Serial.println("iter++");
    iter++;
  }
  MsTimer2::set(1000, flash);
  MsTimer2::start();
  }
*/

void loop ()
{
  RtcDateTime now = Rtc.GetDateTime();
  //Serial.println("  ---=== FLASH ===---");
  
  if (iter % humidityRate == 0)
  {
    //Console.Out.WriteLine("humidityRate");
    //Serial.println("humidityRate");
    getHumidity();
    //humidityRate = 0;
  }
  if (iter % temperatureRate == 0)
  {
    //Console.Out.WriteLine("temperatureRate");
    //Serial.println("temperatureRate and pressure");
    pressTemperature =  bmp.readTemperature();
    getPressure();
    //temperatureRate = 0;
  }

  //getPressure();

  if (iter > maxIter)
  {
    //Console.Out.WriteLine("maxIter");
    //Serial.println("maxIter");
    iter = 0;
    //return;
  }
  else
  {
    //Serial.println("iter++");
    iter++;
  }
  printData(now);  
  delay(1000);
}

void loopOld ()
{
  /*
    if (!Rtc.IsDateTimeValid())
    {
    // Common Cuases:
    //    1) the battery on the device is low or even missing and the power line was disconnected
    Serial.println("RTC lost confidence in the DateTime!");
    }

    RtcDateTime now = Rtc.GetDateTime();
    //getPressure();

    //getHumidity();
    //sensors.requestTemperatures(); // Temp abfragen
    //temperature = sensors.getTempCByIndex(0);
    //Serial.print(sensors.getTempCByIndex(0) );
    //Serial.print(" Grad Celsius");

    printData(now);
    Serial.println();

    //delay(1000*10); // ten seconds
    //int it = 0;
    //do {
    //delay(1000 * 1);
    delay(1000);
    //it++;
    //} while (it < 30);
  */
}
/*
  void adresseAusgeben() {
  byte i;
  byte present = 0;
  byte data[12];
  byte addr[8];

  //Serial.print("Suche 1-Wire-Devices...\n\r");// "\n\r" is NewLine
  while (ourWire.search(addr))
  {
    Serial.print("\n\r\n\r1-Wire-Device gefunden mit Adresse:\n\r");
    for ( i = 0; i < 8; i++) {
      Serial.print("0x");
      if (addr[i] < 16) {
        Serial.print('0');
      }
      Serial.print(addr[i], HEX);
      if (i < 7) {
        Serial.print(", ");
      }
    }
    if ( OneWire::crc8( addr, 7) != addr[7]) {
      Serial.print("CRC is not valid!\n\r");
      return;
    }
  }
  Serial.println();
  ourWire.reset_search();
  return;
  }
*/

void printData(const RtcDateTime& dt)
{
  char datestring[40];
  snprintf_P(datestring,
             countof(datestring),
             PSTR("%02u.%02u.%04u %02u:%02u:%02u"),
             dt.Day(),
             dt.Month(),
             dt.Year(),
             dt.Hour(),
             dt.Minute(),
             dt.Second() );
  Serial.print("BB");
  Serial.print(";");
  Serial.print(datestring);
  Serial.print(";");

  /*
    snprintf_P(datestring,
               countof(datestring),
               PSTR("%02d/%02u/%02f"),
               temperature,
               pressure,
               altitude );
    Serial.print(datestring);
  */

  //  Serial.print(temperature);

  char buf[40];
  sprintf(buf, "%02d", pressure);
  char bufFloat[40];
  Serial.print(buf);
  const int n = 0;
  dtostrf(pressTemperature, 2, n, bufFloat);

  Serial.print(";");
  Serial.print(bufFloat);
  dtostrf(altitude, 2, n, bufFloat);
  Serial.print(";");
  Serial.print(bufFloat);

  /*
    dtostrf(temperature, 2, n, bufFloat);
    Serial.print(";");
    Serial.print(bufFloat);
  */

  Serial.print(";");
  Serial.print(humidity);
  Serial.println(";");
}

void getPressure()
{
  //  pressTemperature =  bmp.readTemperature();
  pressure =  bmp.readPressure() / 133.3224;
  altitude = bmp.readAltitude();
}

char *ftoa(char *a, double f, int precision)
{
  long p[] = {0, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000};

  char *ret = a;
  long heiltal = (long)f;
  itoa(heiltal, a, 10);
  while (*a != '\0') a++;
  *a++ = '.';
  long desimal = abs((long)((f - heiltal) * p[precision]));
  itoa(desimal, a, 10);
  return ret;
}

void getHumidity()
{
  // Задержка 2 секунды между измерениями
  //delay(2000);
  //Считываем влажность
  humidity = dht.readHumidity();
  // Считываем температуру
  //float t = dht.readTemperature();
  // Проверка удачно прошло ли считывание.
  if (isnan(humidity) /*|| isnan(t)*/)
  {
    Serial.println("Не удается считать показания");
    return;
  }
  // Serial.print("Влажность: " + h + " %\t" + "Температура: " + t + " *C ");
  //Serial.println(h);
}


