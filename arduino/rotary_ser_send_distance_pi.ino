// Taken from Github and Commented out
// this is intermittant and i'm not sure why
// try replacing wires

// Wire   | Physical Pin  | Pin Name in program
// Orange --> 3               pin2
// Brown  --> 4               pin3
// Black  --> 2               pin1

int pin1 = 2;
int pin2 = 3;
int pin3 = 4;
//int on_off = 4;
//int units = 5;
//int hld_clr = 6;
//int no1_no1 = 7;

int Pos = 0; 
int State;
int LastState;  

const float pi = 3.14159;
const float R = 7.1882;
const int N = 24;

float distance = 0;
int seq = 0;
void setup() { 
  pinMode (pin1 ,INPUT);
  pinMode (pin2 ,INPUT);
  pinMode (pin3 ,INPUT); // physical pin 4 (brown)
  //pinMode (on_off, OUTPUT);
  //pinMode (units, OUTPUT);
  //pinMode (hld_clr, OUTPUT);
  //pinMode (no1_no1, OUTPUT);

  //attachInterrupt(0, sendPiData, RISING); //Intrupt 0 attached to physical pin 2 (pin1) (Black), comment for debug
  attachInterrupt(1, rotary, CHANGE); // Interupt 1 attached to physical pin 3 (pin2) (Orange)
  Serial.begin(9600); // open the serial port at 9600 bps:
  
  LastState = digitalRead(pin3);  // physical pin 4 (brown)

} 

//void loop(){
//  distance = ((2*pi*R)/N) * Pos ;  
//  Serial.println(-1*distance);
//  delay(10);  
//}

void loop() { 
  distance = -0.01*((2*pi*R)/N) * Pos ; // distance in m
  Serial.println(distance); // uncoment for debug
  delay(10);
}

//void sendPiData(){ // writes to serial when the pi sends a ping // comment for debug
//  Serial.println(int(-1*distance));
//}
 
void rotary(){
  State = digitalRead(pin3); // physical pin 4 (brown)
   if (State != LastState){     
     if (digitalRead(pin2) != State) { // physical pin 3 (orange) 
       Pos ++;
     } 
     
     else {
       Pos --;
     }
   } 
   
 }
