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
#define lowPin 1

void backAndForth (int dirPin, int stepPin);
void setUpMotor (struct& Motor motor1, int dirPin, int stepPin, maxNumSteps);

const int GIVE = 100;
const int MAX_NUM_STEPS = 1600;

struct Motor {
  int dirPin;
  int stepPin;
  int maxNumSteps;
  int currentDirection;
} motor;

void setup() {
  // put your setup code here, to run once:
  pinMode(dirPinBottom, OUTPUT);
  pinMode(stepPinBottom, OUTPUT);
  pinMode(dirPinTop, OUTPUT);
  pinMode(stepPinTop, OUTPUT);
  pinMode(dirPinRight, OUTPUT);
  pinMode(stepPinRight, OUTPUT);
  pinMode(dirPinLeft, OUTPUT);
  pinMode(stepPinLeft, OUTPUT);
  pinMode(dirPinFront, OUTPUT);
  pinMode(stepPinFront, OUTPUT);
  pinMode(dirPinBack, OUTPUT);
  pinMode(stepPinBack, OUTPUT);
  digitalWrite(dirPinBottom, HIGH);
  digitalWrite(dirPinTop, HIGH);
  digitalWrite(dirPinLeft, HIGH);
  digitalWrite(dirPinRight, HIGH);
  digitalWrite(dirPinFront, HIGH);
  digitalWrite(dirPinBack, HIGH);
  digitalWrite(lowPin, LOW);
  pinMode(lowPin, OUTPUT);
}

void loop() {

//backAndForth(dirPinBottom, stepPinBottom);
//backAndForth(dirPinTop, stepPinTop);
//backAndForth(dirPinLeft, stepPinLeft);
//backAndForth(dirPinRight, stepPinRight);
//backAndForth(dirPinFront, stepPinFront);
//backAndForth(dirPinBack, stepPinBack);
}

void setUpMotor (struct Motor motor1, int dirPin, int stepPin, maxNumSteps) {
  
}

void backAndForth (int dirPin, int stepPin) {
  digitalWrite(dirPin, HIGH);

  for (int i = 0; i < 500; i++) {
  digitalWrite(stepPin,HIGH); 
   delayMicroseconds(250); 
   digitalWrite(stepPin,LOW); 
   delayMicroseconds(250); 
  }
  delay(2000);

  digitalWrite(dirPin, LOW);

  for (int i = 0; i < 500; i++) {
  digitalWrite(stepPin,HIGH); 
   delayMicroseconds(250); 
   digitalWrite(stepPin,LOW); 
   delayMicroseconds(250); 
  }
  delay(2000);
}
