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

//void rotateQuarter (motor* motor1);

const int MAX_NUM_STEPS = 1600;
const int STEP_BY = 10;
const int RIGHT_MOTOR = 0;
const int LEFT_MOTOR = 1;
const int UP_MOTOR = 2;
const int DOWN_MOTOR = 3;
const int FRONT_MOTOR = 4;
const int BACK_MOTOR = 5;

typedef struct {
  int dirPin = 0;
  int stepPin = 0;
  int maxNumSteps = 0;
  int currentDirection = HIGH;
  int give = 0;
} motor;

motor motorArry[6];
String command;

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
  Serial.println("calibrate");
  Serial.println("test");
  Serial.println("fast test");
}

void loop() {
  if(Serial.available()){
     command = Serial.readStringUntil('\n');
        if(command.equals("calibrate")){
          calibrateMotors();
          Serial.println("Done Calibrating");
        }
        else if(command.equals("test")){
          for (int i = 0; i < 6; i++) {
            rotateQuarter(&motorArry[i]);
            delay(1000);
            switchDirection(&motorArry[i]);
            rotateQuarter(&motorArry[i]);
            delay(1000);
          }
        }
        if(command.equals("runFastTest")){
          rotateQuarter(&motorArry[1]);
          rotateQuarter(&motorArry[2]);
          rotateQuarter(&motorArry[3]);
          rotateQuarter(&motorArry[4]);
          rotateQuarter(&motorArry[5]);
          rotateQuarter(&motorArry[0]);
          switchDirection(&motorArry[0]);
          rotateQuarter(&motorArry[0]);
          switchDirection(&motorArry[5]);
          rotateQuarter(&motorArry[5]);
          switchDirection(&motorArry[4]);
          rotateQuarter(&motorArry[4]);
          switchDirection(&motorArry[3]);
          rotateQuarter(&motorArry[3]);
          switchDirection(&motorArry[2]);
          rotateQuarter(&motorArry[2]);
          switchDirection(&motorArry[1]);
          rotateQuarter(&motorArry[1]);
          Serial.println("Did it break?");
        }
      Serial.flush();
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

void rotateQuarter (motor* motor1) {
  for (int i = 0; i < (motor1->maxNumSteps / 4); i++) {
  digitalWrite(motor1->stepPin,HIGH); 
   delayMicroseconds(250); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(250); 
  }
}

void rotateSteps (motor* motor1, int numSteps) {
  for (int i = 0; i < numSteps; i++) {
  digitalWrite(motor1->stepPin,HIGH); 
   delayMicroseconds(250); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(250); 
  }
}

void switchDirection (motor* motor1) {
  if (motor1->currentDirection == HIGH) {
    motor1->currentDirection = LOW;
  }
  else {
    motor1->currentDirection = HIGH;
  }
  digitalWrite(motor1->dirPin, motor1->currentDirection);
  for (int i = 0; i < motor1->give; i++) {
  digitalWrite(motor1->stepPin,HIGH); 
   delayMicroseconds(250); 
   digitalWrite(motor1->stepPin,LOW); 
   delayMicroseconds(250); 
  }
}

void adjustMotorPosition (motor* motorPtr) {
  bool bKeepLooping = true;
  bool bHadToBeAdjusted = false;
  int originalDirection = motorPtr->currentDirection;
  
  while (bKeepLooping) {
    if(Serial.available()){
        command = Serial.readStringUntil('\n');
        if(command.equals("+")){
          if (motorPtr->currentDirection == HIGH) {
            switchDirection(motorPtr);
          }
          rotateSteps (motorPtr, STEP_BY);
          bHadToBeAdjusted = true;
        }
        else if(command.equals("-")){
          if (motorPtr->currentDirection == LOW) {
            switchDirection(motorPtr);
          }
          rotateSteps (motorPtr, STEP_BY);
          bHadToBeAdjusted = true;
        }
        else if(command.equals("next")){
            bKeepLooping = false;
        }
        else{
            Serial.println("Invalid command");
        }
    }
  }
  if (motorPtr->currentDirection != originalDirection) {
    switchDirection(motorPtr);
  }
  Serial.flush();
}

void calibrateMotors() {
  Serial.println("Commands:");
  Serial.println("Move Foward: +");
  Serial.println("Move Backwards: -");
  Serial.println("Continue: next");
  for(int i = 0; i < 6; i++) {
    rotateQuarter(&motorArry[i]);
    adjustMotorPosition(&motorArry[i]);
    rotateQuarter(&motorArry[i]);
    delay(2500);
    switchDirection (&motorArry[i]);
    rotateQuarter(&motorArry[i]);
    rotateQuarter(&motorArry[i]);
    delay(2500);
  }
}
