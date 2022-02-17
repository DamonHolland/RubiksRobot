/*
NeoPixel LEDs

modified on 7 May 2019
by Saeed Hosseini @ Electropeak
**This code is based on Adafruit NeoPixel library Example**
https://electropeak.com/learn/

*/

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN      9
#define NUMPIXELS 12


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
pixels.begin();
}

void loop() {
pixels.clear();
pixels.setBrightness(255);
for (int i = 0; i < NUMPIXELS; i++) {
  pixels.setPixelColor(i, pixels.Color(255, 255, 255));
}
pixels.show();
delay(20);
}
