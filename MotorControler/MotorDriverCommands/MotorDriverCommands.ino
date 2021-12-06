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
  Serial.println("Commands:");
  Serial.println("test");
  Serial.println("fast test");
  Serial.println("command input");
  memset(buff, '\0', MAX_COMMAND_SIZE);

}

void loop() {
  if(Serial.available()){
     command = Serial.readStringUntil('\n');
        if(command.equals("command input")){
          int currentPos = 0;
          while(!Serial.available()) {
          }
          command = Serial.readStringUntil('\n');
          command.toCharArray(buff, MAX_COMMAND_SIZE);
          while(parseCommandFromLine(buff, &currentPos)) {
          }
        }
        else if(command.equals("test")){
          for (int i = 0; i < 6; i++) {
            rotateQuarter(&motorArry[i]);
            delay(1000);
            switchDirection(&motorArry[i], true);
            rotateQuarter(&motorArry[i]);
            delay(1000);
          }
        }
        if(command.equals("fast test")){
          rotateQuarter(&motorArry[1]);
          rotateQuarter(&motorArry[2]);
          rotateQuarter(&motorArry[3]);
          rotateQuarter(&motorArry[4]);
          rotateQuarter(&motorArry[5]);
          rotateQuarter(&motorArry[0]);
          switchDirection(&motorArry[0], true);
          rotateQuarter(&motorArry[0]);
          switchDirection(&motorArry[5], true);
          rotateQuarter(&motorArry[5]);
          switchDirection(&motorArry[4], true);
          rotateQuarter(&motorArry[4]);
          switchDirection(&motorArry[3], true);
          rotateQuarter(&motorArry[3]);
          switchDirection(&motorArry[2], true);
          rotateQuarter(&motorArry[2]);
          switchDirection(&motorArry[1], true);
          rotateQuarter(&motorArry[1]);
          Serial.println("Did it break?");
        }
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
   delayMicroseconds(250); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(250); 
  }
}

void rotateStepsParallel (motor* motor1, motor* motor2, int numSteps) {
  for (int i = 0; i < numSteps; i++) {
  digitalWrite(motor1->stepPin,HIGH); 
  digitalWrite(motor2->stepPin,HIGH);
   delayMicroseconds(250); 
   digitalWrite(motor1->stepPin,LOW);
   digitalWrite(motor2->stepPin,LOW);
   delayMicroseconds(250); 
  }
}

void rotateQuarter (motor* motorPtr) {
  for (int i = 0; i < (motorPtr->maxNumSteps / 4); i++) {
  digitalWrite(motorPtr->stepPin,HIGH); 
   delayMicroseconds(DELAY_SPEED / 2); 
   digitalWrite(motorPtr->stepPin,LOW); 
   delayMicroseconds(DELAY_SPEED / 2); 
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
  int steps = 0;
  int numDigits = 0;
  char motor = '!';
  bool returnVal = true;
  bool isNegative = false;
  
  motor = Line[*currentPos];
  (*currentPos) += 1;
  steps = atoi(&Line[*currentPos]);
  while(isDigit(Line[*currentPos]) && *currentPos < 100) {
    *currentPos += 1;
  }
  if(Line[*currentPos] == '\0' || *currentPos == 99) {
    returnVal = false;
  }
  if(steps < 0) {
    isNegative = true;
    steps *= -1;
  }
  Serial.println(motor);
  Serial.println(steps);
  Serial.println(isNegative);
  return returnVal;
}

void runCommand (char motorChar, int steps, bool isNeg) {
  motor* theMotor = findMotor(motorChar);
  switchDirection (theMotor, isNeg);
  rotateSteps(theMotor, steps);
}

void runParallelCommand (char motorChar1, char motorChar2, int steps, bool isNeg1, bool isNeg2) {
  motor* theMotor1 = findMotor(motorChar1);
  motor* theMotor2 = findMotor(motorChar2);
  switchDirection (theMotor1, isNeg1);
  switchDirection (theMotor1, isNeg2);
  rotateStepsParallel(theMotor1, theMotor2, steps);
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
