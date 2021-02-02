int pin1 = 2;
int pin2 = 3;
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

String nigger = "";

float distance = 0;
int seq = 0;
void setup() { 
  pinMode (pin1 ,INPUT);
  pinMode (pin2 ,INPUT);
  pinMode (on_off, OUTPUT);
  pinMode (units, OUTPUT);
  pinMode (hld_clr, OUTPUT);
  pinMode (no1_no1, OUTPUT);
  
 attachInterrupt(1, rotary, CHANGE);
  Serial.begin(9600); // open the serial port at 9600 bps:
  
  LastState = digitalRead(pin1);    

} 

//void loop(){
//  distance = ((2*pi*R)/N) * Pos ;  
//  Serial.println(-1*distance);
//  delay(10);  
//}

void loop() { 
  distance = 0.01*((2*pi*R)/N) * Pos ; // distance in m
  Serial.println(int(-1*distance));
  delay(10);
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
