**These are equivalent statements for an Arduino Uno:**

attachInterrupt(**0**,ISR,CHANGE);

attachInterrupt(**digitalPinToInterrupt(2)**,ISR,CHANGE);


More details:

[Arduino interrupts](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/)
