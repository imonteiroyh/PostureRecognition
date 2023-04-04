#include <CayenneMQTTESP32.h>
#include <DHT.h>

#define CAYENNE_PRINT Serial

char ssid[] = "";
char wifi_password[] = "";

char username[] = "";
char mqtt_password[] = "";
char client_id[] = "";

#define PIN_POWER 17
#define PIN_GND 4

#define PIN_DHT 16
#define DHT_TYPE DHT11

DHT dht(PIN_DHT, DHT_TYPE);
int t;

void setup() {
	Serial.begin(9600);
	Cayenne.begin(username, mqtt_password, client_id, ssid, wifi_password);
	pinMode(PIN_POWER, OUTPUT);
	pinMode(PIN_GND, OUTPUT);
	digitalWrite(PIN_POWER, HIGH);
	digitalWrite(PIN_GND, LOW);
}

void loop() {
	Cayenne.loop(100);
}

CAYENNE_OUT(1){
	CAYENNE_LOG("Channel %u, value %s", request.channel, getValue.asString());
	t = dht.readTemperature();
	Cayenne.celsiusWrite(1, t);
	Serial.printf("Temperatura: %d\n", t);
}