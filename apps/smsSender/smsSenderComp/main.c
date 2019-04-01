#include "legato.h"
#include "interfaces.h"

COMPONENT_INIT
{
  char destination[] = "0695162402";
  char text[] = "Hello. This message is from MangOH. This is for test.";

  le_sms_MsgRef_t myMsg = le_sms_Create();

  le_sms_SetDestination(myMsg, destination);
  le_sms_SetText(myMsg, text);
  le_sms_Send(myMsg);
  le_sms_Delete(myMsg);

}
