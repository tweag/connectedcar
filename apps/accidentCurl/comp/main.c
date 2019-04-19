#include "legato.h"
#include "interfaces.h"
#include <curl/curl.h>

static const char Url[] = "http://192.168.2.3:5000";
static const char FormatStr[] = "/sys/devices/i2c-0/0-0068/iio:device0/in_%s_%s";
static const char AccType[]   = "accel";
static const char CompX[]     = "x_raw";
static const char CompY[]     = "y_raw";
static const char CompZ[]     = "z_raw";
// static const char destination[] = "0695162402";


// void send_message (char *text)
// {
//   le_sms_MsgRef_t myMsg = le_sms_Create();
//   le_sms_SetDestination(myMsg, destination);
//   le_sms_SetText(myMsg, text);
//   le_sms_Send(myMsg);
//   le_sms_Delete(myMsg);
// }



// Curl part
static void PostUrl(char *jsonString)
{

  // send_message(jsonString);

  CURL *curl = curl_easy_init();

  struct curl_slist *hs=NULL;
  hs = curl_slist_append(hs, "Content-Type: application/json");
  curl_easy_setopt(curl, CURLOPT_HTTPHEADER, hs);


    if (curl)
  {
      curl_easy_setopt(curl, CURLOPT_URL, Url);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonString);
      curl_easy_perform(curl);
      curl_easy_cleanup(curl);
  }
}

// Accelration part
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

COMPONENT_INIT
{

  int32_t latitude; int32_t longitude; int32_t horizontalAccuracy;
  int32_t *latitudePtr = &latitude; int32_t *longitudePtr = &longitude; int32_t *horizontalAccuracyPtr = &horizontalAccuracy;

  double accX; double accY; double accZ;
  double *accXPtr = &accX; double *accYPtr = &accY; double *accZPtr = &accZ;
  double a = 0.0;

  double accidentThresh = 30 * 1000;

  double timeoutInSeconds = 1;

  char jsonString[1000];
  int counter = 0;

  time_t startTime = time(NULL);

  while(true)
  {
    if (difftime(time(NULL), startTime) > timeoutInSeconds)
    {
      mangOH_ReadAccelSensor( accXPtr, accYPtr, accZPtr);
      a = pow ( pow(accX,2) + pow(accY,2) + pow(accZ,2) , 0.5 );
      if (a > accidentThresh)
      {
        le_pos_Get2DLocation(latitudePtr, longitudePtr, horizontalAccuracyPtr);
        sprintf(jsonString,"{ \"counter\" :  %d , \"acceleration\" :  %d , \"latitude\" :  %d , \"longitude\" :  %d }",counter , (int)a , latitude , longitude );
        PostUrl(jsonString);

        counter++;
        startTime = time(NULL);
      }
    }
  }
}
