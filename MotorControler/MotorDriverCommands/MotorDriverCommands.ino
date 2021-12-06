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
          parseCommandFromLine(buff, &currentPos);
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
        if(command.equals("fast test")){
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

void rotateQuarter (motor* motorPtr) {
  for (int i = 0; i < (motorPtr->maxNumSteps / 4); i++) {
  digitalWrite(motorPtr->stepPin,HIGH); 
   delayMicroseconds(DELAY_SPEED / 2); 
   digitalWrite(motorPtr->stepPin,LOW); 
   delayMicroseconds(DELAY_SPEED / 2); 
  }
}

void switchDirection (motor* motorPtr) {
  if (motorPtr->currentDirection == HIGH) {
    motorPtr->currentDirection = LOW;
  }
  else {
    motorPtr->currentDirection = HIGH;
  }
  digitalWrite(motorPtr->dirPin, motorPtr->currentDirection);
}

void parseCommandFromLine(const char* Line, int* currentPos) {
  int steps = 0;
  int numDigits = 0;
  int power = 0;
  char motor = '!';
  
  motor = Line[*currentPos];
  *currentPos++;
  while(isDigit(Line[*currentPos])) {
    numDigits++;
    currentPos++;
  }
  for (int i = *currentPos - 1; i > (*currentPos - numDigits - 1); i--) {
    steps += atoi(&Line[i]) * pow(10, power);
    power++;
  }
  Serial.println(motor);
  Serial.println(steps);
}
