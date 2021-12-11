#define dirPinRight 2
#define stepPinRight 8
#define dirPinFront 3
#define stepPinFront 9
#define dirPinBottom 4
#define stepPinBottom 10
#define dirPinLeft 5
#define stepPinLeft 11
#define dirPinBack 6
#define stepPinBack 12
#define dirPinTop 7
#define stepPinTop 13

const int MAX_NUM_STEPS = 1600;
const int DELAY_SPEED = 500;
const int STEP_BY = 10;
const int RIGHT_MOTOR = 0;
const int LEFT_MOTOR = 1;
const int UP_MOTOR = 2;
const int DOWN_MOTOR = 3;
const int FRONT_MOTOR = 4;
const int BACK_MOTOR = 5;
int MAX_COMMAND_SIZE = 100;
int motorDelay = 250;

typedef struct {
  int dirPin = 0;
  int stepPin = 0;
  int maxNumSteps = 0;
  int currentDirection = HIGH;
  int give = 0;
} motor;

motor motorArry[6];
String command;
char buff[100];

void setup() {
   // put your setup code here, to run once:
  Serial.begin(9600);
  setUpMotor(&motorArry[RIGHT_MOTOR], dirPinRight, stepPinRight, MAX_NUM_STEPS, (MAX_NUM_STEPS / 16));
  setUpMotor(&motorArry[LEFT_MOTOR], dirPinLeft, stepPinLeft, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[UP_MOTOR], dirPinTop, stepPinTop, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[DOWN_MOTOR], dirPinBottom, stepPinBottom, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[FRONT_MOTOR], dirPinFront, stepPinFront, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  setUpMotor(&motorArry[BACK_MOTOR], dirPinBack, stepPinBack, MAX_NUM_STEPS, MAX_NUM_STEPS / 16);
  //Serial.println("Commands:");
  //Serial.println("test");
  //Serial.println("fast test");
  //Serial.println("command input");
  memset(buff, '\0', MAX_COMMAND_SIZE);

}

void loop() {
  //Serial.println("you made it");
  if(Serial.available()){
    
          int currentPos = 0;
          while(!Serial.available()) {
          }
          command = Serial.readStringUntil('\n');
          Serial.println(command);
          command.toCharArray(buff, MAX_COMMAND_SIZE);
          while(parseCommandFromLine(buff, &currentPos)) {
          }
          memset(buff, '\0', MAX_COMMAND_SIZE);
          command = "";
   }
}

void setUpMotor (motor* motorPtr, int dirPin, int stepPin, int maxNumSteps, int give) {
  motorPtr->dirPin = dirPin;
  motorPtr->stepPin = stepPin;
  motorPtr->maxNumSteps = maxNumSteps;
  motorPtr->currentDirection = LOW;
  motorPtr->give = give;
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, LOW);
  pinMode(stepPin, OUTPUT);
}

void rotateSteps (motor* motor1, int numSteps) {
  for (int i = 0; i < numSteps; i++) {
  digitalWrite(motor1->stepPin,HIGH); 
   delayMicroseconds(motorDelay); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(motorDelay); 
  }
}

void rotateStepsParallel (motor* motor1, motor* motor2, int numSteps1, int numSteps2) {
  if (numSteps1 == numSteps2) {
    //Serial.println(numSteps1);
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
  while(isDigit(Line[*currentPos]) && *currentPos < 100) {
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
  while(isDigit(Line[*currentPos]) && *currentPos < 100) {
    *currentPos += 1;
  }
  //do both
  *currentPos += 1;
  //Serial.println("Two");
  //Serial.println(motor1);
  //Serial.println(steps1);
  //Serial.println(isNegative1);
  //Serial.println(motor2);
  //Serial.println(steps2);
  //Serial.println(isNegative2);
  runParallelCommand(motor1, motor2, (steps1/90 * 400), (steps2/90 * 400), isNegative1, isNegative2);
  }
  else {
   //do one
   *currentPos += 1;
   //Serial.println("One");
  //Serial.println(motor1);
  //Serial.println(steps1);
  //Serial.println(isNegative1);
  runCommand(motor1, (steps1/90 * 400), isNegative1);
  }
  if(Line[*currentPos] == '\0' || *currentPos == 99 ) {
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
