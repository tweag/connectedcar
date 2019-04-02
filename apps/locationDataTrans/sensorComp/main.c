#include "legato.h"
#include "interfaces.h"

COMPONENT_INIT
{

  int32_t latitude;
  int32_t longitude;
  int32_t horizontalAccuracy;

  int32_t *latitudePtr = &latitude;
  int32_t *longitudePtr = &longitude;
  int32_t *horizontalAccuracyPtr = &horizontalAccuracy;

  le_pos_Get2DLocation(latitudePtr, longitudePtr, horizontalAccuracyPtr);

  char latitudeString[100];
  char longitudeString[100];

  sprintf(latitudeString,"%d", *latitudePtr);
  sprintf(longitudeString,"%d", *longitudePtr);

  char destination[] = "0695162402";
  char text[1000];
  strcpy(text , "Hello. This message is from MangOH.");
  strcat(text, "\nYour latitude: ");
  strcat(text, latitudeString);
  strcat(text, "\nYour longitude: ");
  strcat(text, longitudeString);

  le_sms_MsgRef_t myMsg = le_sms_Create();

  le_sms_SetDestination(myMsg, destination);
  le_sms_SetText(myMsg, text);
  le_sms_Send(myMsg);
  le_sms_Delete(myMsg);

}
