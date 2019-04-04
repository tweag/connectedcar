#include "legato.h"
#include "interfaces.h"


static const char FormatStr[] = "/sys/devices/i2c-0/0-0068/iio:device0/in_%s_%s";
static const char AccType[]   = "accel";
static const char CompX[]     = "x_raw";
static const char CompY[]     = "y_raw";
static const char CompZ[]     = "z_raw";


le_result_t ReadDoubleFromFile
(
    const char *filePath,
    double *value
)
{
    le_result_t r = LE_OK;
    FILE *f = fopen(filePath, "r");
    if (f == NULL)
    {
        LE_WARN("Couldn't open '%s' - %m", filePath);
        r = LE_IO_ERROR;
        goto done;
    }

    int numScanned = fscanf(f, "%lf", value);
    if (numScanned != 1)
    {
        r = LE_FORMAT_ERROR;
    }

    fclose(f);
done:
    return r;
}


void mangOH_ReadAccelSensor(double *xAcc,double *yAcc,double *zAcc)
{
  char path[256];

  snprintf(path, sizeof(path), FormatStr, AccType, CompX);
  ReadDoubleFromFile(path, xAcc);

  snprintf(path, sizeof(path), FormatStr, AccType, CompY);
  ReadDoubleFromFile(path, yAcc);

  snprintf(path, sizeof(path), FormatStr, AccType, CompZ);
  ReadDoubleFromFile(path, zAcc);

}


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

  double accX; double accY; double accZ;
  double *accXPtr = &accX; double *accYPtr = &accY; double *accZPtr = &accZ;
  double a; char aString[10];

  double accidentThresh = 30 * 1000;

  double timeoutInSeconds = 3;

  char destination[] = "0695162402";
  char text[1000];
  int counter = 0; char counterString[10];

  time_t startTime = time(NULL);

  while(true)
  {
    if (difftime(time(NULL), startTime) > timeoutInSeconds)
    {
      mangOH_ReadAccelSensor( accXPtr, accYPtr, accZPtr);
      a = pow ( pow(accX,2) + pow(accY,2) + pow(accZ,2) , 0.5 );
      if (a > accidentThresh)
      {
        sprintf(counterString,"%d", counter);
        sprintf(aString,"%f", a);
        strcpy (text , "Hello from Tweag :) . A drastic accelaration is detected, be careful!\nHere is the counter number: ");
        strcat (text , counterString );
        strcat (text , "\nAcceleration is: " );
        strcat (text , aString );

        send_message (destination , text);
        counter++;
        startTime = time(NULL);
      }
    }
  }




  mangOH_ReadAccelSensor(accXPtr,accYPtr,accZPtr);




}
