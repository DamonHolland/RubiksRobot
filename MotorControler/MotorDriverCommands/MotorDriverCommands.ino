#include <TM1637Display.h>
#include <Adafruit_NeoPixel.h>
#define dirPinRight 45
#define stepPinRight 43
#define enPinRight 47
#define dirPinFront 36
#define stepPinFront 34
#define enPinFront 38
#define dirPinBottom 51
#define stepPinBottom 49
#define enPinBottom 53
#define dirPinLeft 30
#define stepPinLeft 28
#define enPinLeft 32
#define dirPinBack 25
#define stepPinBack 23
#define enPinBack 27
#define dirPinTop 24
#define stepPinTop 22
#define enPinTop 26
#define CLK1 29
#define DIO1 31
#define CLK2 33
#define DIO2 35
#define bttn1 39
#define bttn2 41
#define lightPin 37
#define NUMPIXELS 12

Adafruit_NeoPixel lights = Adafruit_NeoPixel(NUMPIXELS, lightPin, NEO_GRB + NEO_KHZ800);

const int MAX_NUM_STEPS = 1600;
const int DELAY_SPEED = 500;
const int STEP_BY = 10;
const int RIGHT_MOTOR = 0;
const int LEFT_MOTOR = 1;
const int UP_MOTOR = 2;
const int DOWN_MOTOR = 3;
const int FRONT_MOTOR = 4;
const int BACK_MOTOR = 5;
int MAX_COMMAND_SIZE = 500;
int motorDelay = 250;
unsigned long startTime;
unsigned long currentTime;
unsigned long endTime;
int numMoves = 0;
int coolDown = 0;

// Create display object of type TM1637Display:
TM1637Display display1 = TM1637Display(CLK1, DIO1);
TM1637Display display2 = TM1637Display(CLK2, DIO2);

// Create array that turns all segments on:
const uint8_t data[] = {0xff, 0xff, 0xff, 0xff};

// Create array that turns all segments off:
const uint8_t blank[] = {0x00, 0x00, 0x00, 0x00};

// You can set the individual segments per digit to spell words or create other symbols:
const uint8_t wait[] = {
  SEG_B | SEG_C | SEG_D | SEG_E | SEG_F | SEG_G,           // w
};

const uint8_t red[] = {
  SEG_A | SEG_C | SEG_D | SEG_E | SEG_F,           // g
};

typedef struct {
  int dirPin = 0;
  int stepPin = 0;
  int enPin = 0;
  int maxNumSteps = 0;
  int currentDirection = HIGH;
  int give = 0;
} motor;

motor motorArry[6];
char buff[500];

void setup() {
   // put your setup code here, to run once:
  Serial.begin(9600);
  setUpMotor(&motorArry[RIGHT_MOTOR], dirPinRight, stepPinRight, enPinRight, MAX_NUM_STEPS, (MAX_NUM_STEPS / 16));
  setUpMotor(&motorArry[LEFT_MOTOR], dirPinLeft, stepPinLeft, enPinLeft, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[UP_MOTOR], dirPinTop, stepPinTop,enPinTop, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[DOWN_MOTOR], dirPinBottom, stepPinBottom, enPinBottom, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[FRONT_MOTOR], dirPinFront, stepPinFront, enPinFront, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[BACK_MOTOR], dirPinBack, stepPinBack, enPinBack, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  memset(buff, '\0', MAX_COMMAND_SIZE);
  pinMode(bttn1, OUTPUT);
  pinMode(bttn2, OUTPUT);
  display1.setBrightness(7);
  display2.setBrightness(7);
  display1.setSegments(data);
  display2.setSegments(data);
  clearTimer();
  delay(1000);
  startTimer();
  lights.begin();
}

void loop() {
  if(Serial.available() > 0){
    int currentPos = 0;
    int hol = 0;
    hol = Serial.read();
    while(hol != 10 && currentPos < MAX_COMMAND_SIZE) {
      if (Serial.available() > 0) {
        if (hol != -1) {
          buff[currentPos] = (char)hol;
          currentPos++;
        }
      hol = Serial.read();
    }
  }

  if (strstr(buff, "lights")) {
    char* walk = buff;
    while (*walk != ' '){
      walk++;
    }
    walk++;
    turnLightsOn(atoi(walk));
    memset(buff, '\0', MAX_COMMAND_SIZE);
  }
  else {
    clearTimer();
    display2.setSegments(blank);
    display2.setSegments(wait);
    currentPos = 0;
    display2.setSegments(blank);
    display2.setSegments(red);
    if (strstr(buff, "-w")) {
      while(digitalRead(bttn1) == LOW){};
      startTimer();
      while(parseCommandFromLine(buff, &currentPos)) {
      }
    }
    else {
      startTimer();
      while(parseCommandFromLine(buff, &currentPos)) {
      }
    }
    endTimer();
    memset(buff, '\0', MAX_COMMAND_SIZE);
  }
          
  }
  else if (digitalRead(bttn2) == HIGH && coolDown + 1000 < millis()) {
    Serial.write("Scramble\n");
    coolDown = millis();
  }
  else if (digitalRead(bttn1) == HIGH && coolDown + 1000 < millis()) {
    Serial.write("Solve\n");
    coolDown = millis();
  }
}

void setUpMotor (motor* motorPtr, int dirPin, int stepPin, int enPin, int maxNumSteps, int give) {
  motorPtr->dirPin = dirPin;
  motorPtr->enPin = enPin;
  motorPtr->stepPin = stepPin;
  motorPtr->maxNumSteps = maxNumSteps;
  motorPtr->currentDirection = LOW;
  motorPtr->give = give;
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, LOW);
  pinMode(stepPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, HIGH);
}

void rotateSteps (motor* motor1, int numSteps) {
  digitalWrite(motor1->enPin, LOW);
  for (int i = 0; i < numSteps; i++) {
  digitalWrite(motor1->stepPin,HIGH); 
   delayMicroseconds(motorDelay); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(motorDelay); 
  }
  digitalWrite(motor1->enPin, HIGH);
}

void rotateStepsParallel (motor* motor1, motor* motor2, int numSteps1, int numSteps2) {
  digitalWrite(motor1->enPin, LOW);
  digitalWrite(motor2->enPin, LOW);
  if (numSteps1 == numSteps2) {
    for (int i = 0; i < numSteps1; i++) {
    digitalWrite(motor1->stepPin,HIGH); 
    digitalWrite(motor2->stepPin,HIGH);
    delayMicroseconds(motorDelay); 
    digitalWrite(motor1->stepPin,LOW);
    digitalWrite(motor2->stepPin,LOW);
    delayMicroseconds(motorDelay); 
  }
  }
  else if (numSteps1 > numSteps2) {
    int diff = numSteps1 - numSteps2;
    for (int i = 0; i < numSteps2; i++) {
      digitalWrite(motor1->stepPin,HIGH); 
      digitalWrite(motor2->stepPin,HIGH);
      delayMicroseconds(motorDelay); 
      digitalWrite(motor1->stepPin,LOW);
      digitalWrite(motor2->stepPin,LOW);
      delayMicroseconds(motorDelay); 
    }
    for (int i = 0; i < diff; i++) {
      digitalWrite(motor1->stepPin,HIGH); 
      delayMicroseconds(motorDelay); 
      digitalWrite(motor1->stepPin,LOW);
      delayMicroseconds(motorDelay); 
    }
  }
  else {
   int diff = numSteps2 - numSteps1;
    for (int i = 0; i < numSteps1; i++) {
      digitalWrite(motor1->stepPin,HIGH); 
      digitalWrite(motor2->stepPin,HIGH);
      delayMicroseconds(motorDelay); 
      digitalWrite(motor1->stepPin,LOW);
      digitalWrite(motor2->stepPin,LOW);
      delayMicroseconds(motorDelay); 
    }
    for (int i = 0; i < diff; i++) {
      digitalWrite(motor2->stepPin,HIGH); 
      delayMicroseconds(motorDelay); 
      digitalWrite(motor2->stepPin,LOW);
      delayMicroseconds(motorDelay); 
    }
  }
  digitalWrite(motor1->enPin, HIGH);
  digitalWrite(motor2->enPin, HIGH);
}

void rotateQuarter (motor* motorPtr) {
  for (int i = 0; i < (motorPtr->maxNumSteps / 4); i++) {
  digitalWrite(motorPtr->stepPin,HIGH); 
   delayMicroseconds(motorDelay); 
   digitalWrite(motorPtr->stepPin,LOW); 
   delayMicroseconds(motorDelay); 
  }
}

void switchDirection (motor* motorPtr, bool isNegative) {
  if (motorPtr->currentDirection == HIGH && isNegative) {
    motorPtr->currentDirection = LOW;
  }
  else if (motorPtr->currentDirection == LOW && !isNegative){
    motorPtr->currentDirection = HIGH;
  }
  digitalWrite(motorPtr->dirPin, motorPtr->currentDirection);
}

bool parseCommandFromLine(const char* Line, int* currentPos) {
  int steps1 = 0;
  int steps2 = 0;
  char motor1 = '!';
  char motor2 = '!';
  bool returnVal = true;
  bool isNegative1 = false;
  bool isNegative2 = false;
  if (*currentPos == 0) {
    motorDelay = atoi(&Line[*currentPos]);
    while (isDigit(Line[*currentPos]) || Line[*currentPos] == ' ') {
    (*currentPos) += 1;
  }
  }
  
  motor1 = Line[*currentPos];
  (*currentPos) += 1;
  if(!isDigit(Line[*currentPos])) {
    if(Line[*currentPos] == '-') {
      isNegative1 = true;
      *currentPos +=1;
    }
  }
  steps1 = atoi(&Line[*currentPos]);
  while(isDigit(Line[*currentPos]) && *currentPos < MAX_COMMAND_SIZE) {
    *currentPos += 1;
  }
  if (isAlpha(Line[*currentPos])) {
   motor2 = Line[*currentPos];
  (*currentPos) += 1;
  if(!isDigit(Line[*currentPos])) {
    if(Line[*currentPos] == '-') {
      isNegative2 = true;
      *currentPos +=1;
    }
  }
  steps2 = atoi(&Line[*currentPos]);
  while(isDigit(Line[*currentPos]) && *currentPos < MAX_COMMAND_SIZE) {
    *currentPos += 1;
  }
  //do both
  *currentPos += 1;
  numMoves++;
  runParallelCommand(motor1, motor2, (steps1/90 * 400), (steps2/90 * 400), isNegative1, isNegative2);
  }
  else {
   //do one
   *currentPos += 1;
   numMoves++;
  runCommand(motor1, (steps1/90 * 400), isNegative1);
  }
  if(Line[*currentPos] == '\0' || *currentPos == MAX_COMMAND_SIZE - 1 ) {
    returnVal = false;
  }
  
  return returnVal;
}

void runCommand (char motorChar, int steps, bool isNeg) {
  motor* theMotor = findMotor(motorChar);
  switchDirection (theMotor, isNeg);
  rotateSteps(theMotor, steps);
}

void runParallelCommand (char motorChar1, char motorChar2, int steps1, int steps2, bool isNeg1, bool isNeg2) {
  motor* theMotor1 = findMotor(motorChar1);
  motor* theMotor2 = findMotor(motorChar2);
  switchDirection (theMotor1, isNeg1);
  switchDirection (theMotor2, isNeg2);
  rotateStepsParallel(theMotor1, theMotor2, steps1, steps2);
}

motor* findMotor (char motorChar) {
  motor* theMotor = NULL;

  switch(motorChar) {
    case 'R':
    theMotor = &motorArry[RIGHT_MOTOR];
    break;
    case 'L': 
    theMotor = &motorArry[LEFT_MOTOR];
    break;
    case 'U': 
    theMotor = &motorArry[UP_MOTOR];
    break;
    case 'D': 
    theMotor = &motorArry[DOWN_MOTOR];
    break;
    case 'F': 
    theMotor = &motorArry[FRONT_MOTOR];
    break;
    case 'B': 
    theMotor = &motorArry[BACK_MOTOR];
    break;
  };
  return theMotor;
}

void startTimer() {
  startTime = millis() / 10.0;
  endTime = millis() / 10.0;
  currentTime = 0;
  display1.showNumberDecEx(currentTime, 0b01000000, true);
}

void endTimer() {
  endTime = (millis() / 10.0) - startTime;
  display1.showNumberDecEx(endTime, 0b01000000, true);
  display2.showNumberDecEx(numMoves, false);
  numMoves = 0;
}

void clearTimer() {
  display1.showNumberDecEx(0, 0b01000000, true);
  display2.showNumberDecEx(0, false);
  numMoves = 0;
}

void scrambleCube() {
  for (int i = 0; i < 20; i++) {
    rotateSteps(&motorArry[random(6)], 400);
  }
}

void turnLightsOn(int brightness) {
  for(int i=0;i<NUMPIXELS;i++){

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    lights.setPixelColor(i,255, 255, 255, 127); // Moderately bright green color.
    lights.setBrightness(brightness);
    lights.show(); // This sends the updated pixel color to the hardware.

  }
}
