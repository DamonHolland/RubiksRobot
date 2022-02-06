/* Example code for TM1637 4 digit 7 segment display with Arduino. More info: www.www.makerguides.com */

unsigned long startTime;
unsigned long currentTime;
unsigned long endTime;
// Include the library:
#include <TM1637Display.h>

// Define the connections pins:
#define CLK 2
#define DIO 3

// Create display object of type TM1637Display:
TM1637Display display = TM1637Display(CLK, DIO);

// Create array that turns all segments on:
const uint8_t data[] = {0xff, 0xff, 0xff, 0xff};

// Create array that turns all segments off:
const uint8_t blank[] = {0x00, 0x00, 0x00, 0x00};

// You can set the individual segments per digit to spell words or create other symbols:
const uint8_t done[] = {
  SEG_B | SEG_C | SEG_D | SEG_E | SEG_G,           // d
  SEG_A | SEG_B | SEG_C | SEG_D | SEG_E | SEG_F,   // O
  SEG_C | SEG_E | SEG_G,                           // n
  SEG_A | SEG_D | SEG_E | SEG_F | SEG_G            // E
};

void setup() {
  // Clear the display:
  display.clear();
  delay(1000);
  Serial.begin(9600);
}

void loop() {
  // Set the brightness:
  display.setBrightness(7);
  // All segments on:
  display.setSegments(data);

  delay(1000);
  display.clear();
  delay(1000);
  startTimer();
  // Show counter:
  int i;
  for (i = 0; i < 101; i++) {
    updateTimer();
    currentTime = (millis() / 10.0) - startTime;
    display.showNumberDecEx(currentTime, 0b01000000, true);
    Serial.println(currentTime);
    delay(50);
  }
  endTimer();
  delay(1000);
  display.clear();
  delay(1000);
  
}

void startTimer() {
  startTime = millis() / 10.0;
  endTime = millis() / 10.0;
  currentTime = 0;
  display.showNumberDecEx(currentTime, 0b01000000, true);
}

void updateTimer() {
  currentTime = (millis() / 10.0) - startTime;
  display.showNumberDecEx(currentTime, 0b01000000, true);
}

void endTimer() {
  endTime = currentTime;
  display.showNumberDecEx(endTime, 0b01000000, true);
}
