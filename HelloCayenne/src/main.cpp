#include <CayenneMQTTESP32.h>
#include <DHT.h>
#include <Ultrasonic.h>

#include "config.h"

#define CAYENNE_PRINT Serial
#define TEMPERATURE_CHANNEL 1
#define HUMIDITY_CHANNEL 2
#define PROXIMITY_CHANNEL 3
#define LED_CHANNEL 4

#define PIN_DHT 16
#define DHT_TYPE DHT11

#define SR04_ECHO 27
#define SR04_TRIGGER 14
#define PRESENCE_THRESHOLD 30

#define PIN_LED 13

DHT dht(PIN_DHT, DHT_TYPE);
int temperature, humidity;

Ultrasonic ultrasonic(SR04_TRIGGER, SR04_ECHO);
float distance;
bool presenceDetected;

void readTemperatureAndHumidity(){
	do{
		temperature = (int)dht.readTemperature();
		humidity = (int)dht.readHumidity();
	} while(isnan(temperature) || isnan(humidity));

	Serial.printf("Temperatura: %d / Umidade: %d %%\n", temperature, humidity);
}

void readDistance(){
	long microsec = ultrasonic.timing();
	distance = ultrasonic.convert(microsec, Ultrasonic::CM);
}

bool detectPresence(){
	if(distance <= PRESENCE_THRESHOLD)
		return true;
	else
		return false;
}

void setup() {
	Serial.begin(9600);
	Cayenne.begin(username, mqtt_password, client_id, ssid, wifi_password);
	dht.begin();
	pinMode(PIN_LED, OUTPUT);
	digitalWrite(PIN_LED, LOW);
}

void loop() {
	Cayenne.loop();
	readTemperatureAndHumidity();
	Cayenne.celsiusWrite(TEMPERATURE_CHANNEL, temperature);
	Cayenne.virtualWrite(HUMIDITY_CHANNEL, humidity);

	readDistance();
	presenceDetected = detectPresence();
	Serial.printf("Presença: %d\n", (int)presenceDetected);
	Cayenne.digitalSensorWrite(PROXIMITY_CHANNEL, presenceDetected);
	sleep(2);
}

CAYENNE_IN(LED_CHANNEL){
	digitalWrite(PIN_LED, getValue.asInt());
}