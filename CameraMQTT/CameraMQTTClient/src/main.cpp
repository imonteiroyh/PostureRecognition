#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include "OV7670.h"
#include "config.h"

const int SIOD = 21; //SDA
const int SIOC = 22; //SCL

const int VSYNC = 34;
const int HREF = 35;

const int XCLK = 32;
const int PCLK = 33;

const int D0 = 16;
const int D1 = 17;
const int D2 = 4;
const int D3 = 2;
const int D4 = 15;
const int D5 = 5;
const int D6 = 18;
const int D7 = 23;

OV7670* camera;

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
	
	Serial.begin(9600);
	Serial.println("ESP started");

	Serial.println("Connecting to WiFi...");
	
	WiFi.begin(SSID, WIFI_PASSWORD);
	while(WiFi.status() != WL_CONNECTED){
		delay(100);	
	}

	Serial.println("Connected!");

	client.setServer(BROKER_IP, 1883);

	do {
		client.connect("ESP32");
	} while (!client.connected());

	camera = new OV7670(OV7670::Mode::QQQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);
}

void loop() {
	Serial.println("Entrando no loop");
	camera->oneFrame();

	// int i = 0;

	// int xres = camera->xres;
	// int yres = camera->yres;
	// for(int x = 0 ; x < xres ; x++){
	// 	for(int y = 0 ; y < yres ; y++){

	// 	}
	// }

	sleep(2);
	Serial.println("Saindo do loop");
}