int letters[][50] = 
{
  {1,4,7,10,13,1,2,6,9,12,15,7,8,9,-1,-1,-1},
  {1,3,5,7,9,11}
};
int totalLetters = 2;
int letterLengths[26] = {10, 6}; //rest 0
int lengths[][50] = {
  {200, 200, 200, 200, 200, 200,200, 200, 200, 200, 200, 200, 200, 200},
  {200, 200, 200, 200, 200}
};

int pin_port[16] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 };

int pwm_pin[64] = { 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }; //rest 0
int pin_power[64] = {0}; //all 0

int target = 0;
int totalVoltage = 2;

int minPWM = 110;
int maxPWM = 255;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

bool inRange(int id, int target) {
  if (id < 0) return false;
  if (id >= letterLengths[target]) return false;
  return true;
}

void loop() {
  //turn off everything
  for (int k = 0; k<16; k++) {
    if (pwm_pin[pin_port[k]] == 0) digitalWrite(pin_port[k], LOW);
    else analogWrite(pin_port[k], 0);
  }
  
  
  target = rand() % totalLetters;
  //pick a letter, one loop is one letter

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
        pin_power[prev] -= 1;

      if (inRange(curr, target)) //so we can use -1 to say "no pin gets full power this turn right now"
        pin_power[curr] += 1;
      
      if (inRange(next, target)) 
        pin_power[next] += 1;

      for (int adjuster=prev; adjuster <=next; adjuster++) {
        if (pwm_pin[pin_port[adjuster]] == 1) 
          analogWrite(pin_port[letters[target][adjuster]], minPWM + ((maxPWM-minPWM) * pin_power[adjuster]) / 10 );
        else {
          if (pin_power[adjuster] >= 5)
            digitalWrite(pin_port[letters[target][adjuster]], HIGH);
          else 
            digitalWrite(pin_port[letters[target][adjuster]], LOW);
        }
      }

      // we know that we have 5 power swaps per step
      // so the total time should be as specified in lengths[target][i]
      delay(lengths[target][i] / 5); 
    }
  }
}
