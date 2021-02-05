int piReadyPin = 2;
int pin1 = 3;
int pin2 = 4;

int on_off = 4;
int units = 5;
int hld_clr = 6;
int no1_no1 = 7;

int Pos = 0; 
int State;
int LastState;  

const float pi = 3.14159;

const float R = 7.1882;
const int N = 24;
int sleeper = 0;
boolean mftState = false;

float distance = 0;
int seq = 0;
void setup() { 
  pinMode (pin1 ,INPUT);
  pinMode (pin2 ,INPUT);
  pinMode (on_off, OUTPUT);
  pinMode (units, OUTPUT);
  pinMode (hld_clr, OUTPUT);
  pinMode (no1_no1, OUTPUT);
  
  attachInterrupt(0, sendPiData, RISING);
  attachInterrupt(1, rotary, CHANGE);
  
  Serial.begin(9600); // open the serial port at 9600 bps:
  
  LastState = digitalRead(pin1);    

} 

void loop() { 

  distance = ( -((2*pi*R)/N) * Pos / 100 );  
  delay(10);
  sleeper++;
  if (sleeper==100){
    sleeper = 0;
    mftState = !mftState;
    if (mftState) {digitalWrite(units, HIGH);}
    else {digitalWrite(units, LOW);}
  }
  
}

void sendPiData(){
  Serial.println(int(1*distance));
}
 
void rotary(){
  State = digitalRead(pin1);
   if (State != LastState){     
     if (digitalRead(pin2) != State) { 
       Pos ++;
     } 
     
     else {
       Pos --;
     }
   } 
   
 }
