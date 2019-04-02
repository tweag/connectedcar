#include "legato.h"
#include "interfaces.h"


static const char PressureFile[] = "/sys/devices/i2c-0/0-0076/iio:device1/in_pressure_input";

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


le_result_t mangOH_ReadPressureSensor
(
    double *reading
)
{
    return ReadDoubleFromFile(PressureFile, reading);
}


COMPONENT_INIT
{

  double pressure;
  double *pressurePtr = &pressure;
  mangOH_ReadPressureSensor(pressurePtr);

  char pressureString[1000];

  sprintf(pressureString,"%f", pressure);

  char destination[] = "0695590670";
  char text[1000];
  strcpy(text , "Hello. This message is from MangOH.");
  strcat(text, "The air pressure in Tweag office is\n");
  strcat(text, pressureString);

  le_sms_MsgRef_t myMsg = le_sms_Create();

  le_sms_SetDestination(myMsg, destination);
  le_sms_SetText(myMsg, text);
  le_sms_Send(myMsg);
  le_sms_Delete(myMsg);

}
