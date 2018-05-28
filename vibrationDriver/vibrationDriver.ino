int DELAY = 200;
int letters[][50] =
{
  {1,4,7,10,13,-1,-1,1,2,6,9,12,15,-1,-1,7,8,9,-1,-1,-1},
  {-1, -1,-1, 3,2,1,-1,-1,1,2,3, -1, -1, -1}
};
int totalLetters = 2;
int letterLengths[26] = {21, 14, 14, 14, 14}; //rest 0
int lengths[][50] = {
  {200, 200, 200, 200, 200, 200, 200,200, 200, 200, 200, 200, 200, 200,200, 200, 200, 200, 200, 200, 200},
  {200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200}
};

int pin_port[16] = {0, 22, 24, 26};

int pwm_pin[64] = { 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1 }; //rest 0
int pin_power[64] = {0}; //all 0

int target = 0;

int minPWM = 110;
int maxPWM = 255;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i=0; i<64; i++)
    pinMode(i, OUTPUT);
}

bool inRange(int id, int target) {
  if (id < 0) return false;
  if (id >= letterLengths[target]) return false;
  return true;
}


void writeLetter(int target)
{
  int pin = -1;
  
  for(int i = 0; i < letterLengths[target]; i++) {
    pin = pin_port[letters[target][i]];
    digitalWrite(pin, HIGH);
    delay(DELAY);

  Serial.print("DEBUG, pin: ");
  Serial.println(pin);
    if(i > 0) {
      pin = pin_port[letters[target][i-1]];
      digitalWrite(pin, LOW);
    }
  }

  return;

  /*
  for (int i=0; i<letterLengths[target]; i++) {
    int prev = i-1, curr = i, next = i+1;
    // if it's the first frame, ramp up only the first target pin to 50%
    // assumes the sequence doesn't start with -1
    if (i == 0) {
      while (pin_power[curr] < 5) {
        pin_power[curr] += 1;
      }
    }
    //do 10% increments of vibration swap with current letter (the next letter will start at 50% when this starts!)
    while (pin_power[curr] < 10) {
      if (inRange(prev, target))
        pin_power[prev] -= 2;

      if (inRange(curr, target)) //so we can use -1 to say "no pin gets full power this turn right now"
        pin_power[curr] += 1;

      if (inRange(next, target))
        pin_power[next] += 1;

      for (int adjuster=0; adjuster <letterLengths[target]; adjuster++) {
        int targetpin = letters[target][adjuster];
        if (targetpin > 0) {
          if (pwm_pin[pin_port[targetpin]] == 1) {
            analogWrite(pin_port[targetpin], minPWM + ((maxPWM-minPWM) * pin_power[adjuster]) / 10 );
          }
          else {
            if (pin_power[adjuster] >= 5)
              digitalWrite(pin_port[targetpin], HIGH);
            else
              digitalWrite(pin_port[targetpin], LOW);
          }
        }
      }
      
      Serial.print("Index: ");
      Serial.print(curr);
      Serial.print(", ");
      Serial.print("Phase: ");
      Serial.print(pin_power[curr] - 5);
      Serial.print(" -> ");
      for (int i=0; i<letterLengths[target]; i++) {
        if(pin_power[i] >= 5) {
                Serial.print("1");
        } else {
          Serial.print("0");
        }
        Serial.print(", ");
      }
      Serial.println();

      // we know that we have 5 power swaps per step
      // so the total time should be as specified in lengths[target][i]
      delay(lengths[target][i] / 3);
    }

  }
  */
}
void loop() {
  //turn off everything
  for (int k = 0; k<16; k++) {
    if (pwm_pin[pin_port[k]] == 0) digitalWrite(pin_port[k], LOW);
    else analogWrite(pin_port[k], 0);
  }
  for (int k=0; k<64; k++) {
    pin_power[k] = 0;
  }

  delay(2000);


  //target = rand() % totalLetters;
  target = 1;
  writeLetter(target);

}
