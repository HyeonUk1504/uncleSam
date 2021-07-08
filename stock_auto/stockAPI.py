import os
import sys
import urllib.request
import json
from pprint import pprint

def translate (name):

    client_id = "DNfBbmawwgCd2sq6OXcm" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "4Fci6pnp2C" # 개발자센터에서 발급받은 Client Secret 값

    encText = urllib.parse.quote(name)
    data = "source=ko&target=en&text=" + encText

    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        # print(response_body.decode('utf-8'))

        res = json.loads(response_body.decode('utf-8'))
        print(res['message']['result']['translatedText'])
        return res['message']['result']['translatedText']
    else:
        print("Error Code:" + rescode)

        return name