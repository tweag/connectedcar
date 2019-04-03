#include "legato.h"
#include "interfaces.h"


void send_message (char *destination , char *text)
{
  le_sms_MsgRef_t myMsg = le_sms_Create();
  le_sms_SetDestination(myMsg, destination);
  le_sms_SetText(myMsg, text);
  le_sms_Send(myMsg);
  le_sms_Delete(myMsg);
}

COMPONENT_INIT
{
  double timeoutInSeconds = 10;

  char destination[] = "0695162402";
  char text[100];
  int counter=0;
  char counterString[10];


  time_t startTime = time(NULL);

  while(true)
  {
    if (difftime(time(NULL), startTime) > timeoutInSeconds)
    {
      sprintf(counterString,"%d", counter);
      strcpy (text , "Hello. This is the number of message: ");
      strcat (text , counterString );
      send_message (destination , text);
      counter++;
      startTime = time(NULL);
    }
  }
}
