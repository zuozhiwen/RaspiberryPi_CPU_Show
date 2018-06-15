#include <wiringPi.h>
int main (void)
{
  wiringPiSetup () ;
  pinMode (7, OUTPUT) ;
  for (;;)
  {
    digitalWrite (7, HIGH) ;
    delay (500) ;
    digitalWrite (7,  LOW) ; 
    delay (500) ;
  }
  return 0 ;
}

