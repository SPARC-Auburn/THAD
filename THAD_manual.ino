#define RIGHT_PIN 6
#define LEFT_PIN 7
#define DOWN_PIN 5
#define UP_PIN 4
#define FIRE_PIN 2
#define PRIME_PIN 3

#define ROW_0 8
#define ROW_1 9
#define ROW_2 10
#define COL_0 11
#define COL_1 12

#define DELAY 1   //delay in ms for the signal to propgate through the board



void setup() {
  Serial.begin(9600);
  // set up pins for controlling the relays and set to HIGH
  pinMode(RIGHT_PIN, OUTPUT);
  pinMode(LEFT_PIN, OUTPUT);
  pinMode(UP_PIN, OUTPUT);
  pinMode(DOWN_PIN, OUTPUT);
  pinMode(FIRE_PIN, OUTPUT);
  pinMode(PRIME_PIN, OUTPUT);
  digitalWrite(RIGHT_PIN, HIGH);
  digitalWrite(LEFT_PIN, HIGH);
  digitalWrite(UP_PIN, HIGH);
  digitalWrite(DOWN_PIN, HIGH);
  digitalWrite(FIRE_PIN, HIGH);
  digitalWrite(PRIME_PIN, HIGH);

  // set up pins for reading the pushbut

}

void loop() {

        char inChar = Serial.read();
        if(inChar == 'w')
        {
          digitalWrite(UP_PIN, LOW);
        }
        else if(inChar == 't')
        {
          digitalWrite(UP_PIN, HIGH);
        }
        else if(inChar == 's')
        {
          digitalWrite(DOWN_PIN, LOW);
        }
        else if(inChar == 'g')
        {
          digitalWrite(DOWN_PIN, HIGH);
        }
        else if(inChar == 'a')
        {
          digitalWrite(LEFT_PIN, LOW);
        }
        else if(inChar == 'f')
        {
          digitalWrite(LEFT_PIN, HIGH);
        }
        else if(inChar == 'd')
        {
          digitalWrite(RIGHT_PIN, LOW);
        }
        else if(inChar == 'h')
        {
          digitalWrite(RIGHT_PIN, HIGH);
        }

        if(inChar == 'q')
        {
          digitalWrite(PRIME_PIN, LOW);
          delay(1000);
          digitalWrite(FIRE_PIN, LOW);
          delay(1000);
          digitalWrite(PRIME_PIN, HIGH);
          digitalWrite(FIRE_PIN, HIGH);
        }
}
