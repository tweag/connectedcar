#include "legato.h"
#include <curl/curl.h>

static const char * Url = "http://192.168.2.3:5000";

static void PostUrl(void)
{
  CURL *curl = curl_easy_init();

  struct curl_slist *hs=NULL;
  hs = curl_slist_append(hs, "Content-Type: application/json");
  curl_easy_setopt(curl, CURLOPT_HTTPHEADER, hs);


    if (curl)
  {
      curl_easy_setopt(curl, CURLOPT_URL, Url);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "{\"name\" : \"tweag\"}" );
      curl_easy_perform(curl);
      curl_easy_cleanup(curl);
  }

}

COMPONENT_INIT
{
    PostUrl();
}
