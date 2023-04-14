#include <CayenneMQTTESP32.h>
#include <DHT.h>
#include <Ultrasonic.h>

#include "config.h"

#define CAYENNE_PRINT Serial
#define TEMPERATURE_CHANNEL 1
#define HUMIDITY_CHANNEL 2
#define PROXIMITY_CHANNEL 3

#define PIN_DHT 16
#define DHT_TYPE DHT11

#define SR04_ECHO 12
#define SR04_TRIGGER 13

DHT dht(PIN_DHT, DHT_TYPE);
int temperature, humidity;

Ultrasonic ultrasonic(SR04_TRIGGER, SR04_ECHO);
float distance;

void readTemperatureAndHumidity(){
	do{
		temperature = (int)dht.readTemperature();
		humidity = (int)dht.readHumidity();
	} while(isnan(temperature) || isnan(humidity));

	Serial.printf("Temperatura: %d / Umidade: %d %%\n", temperature, humidity);
}

void setup() {
	Serial.begin(9600);
	Cayenne.begin(username, mqtt_password, client_id, ssid, wifi_password);
	dht.begin();
}

void loop() {
	Cayenne.loop();
	readTemperatureAndHumidity();
	Cayenne.celsiusWrite(TEMPERATURE_CHANNEL, temperature);
	Cayenne.virtualWrite(HUMIDITY_CHANNEL, humidity);

	sleep(2);
}