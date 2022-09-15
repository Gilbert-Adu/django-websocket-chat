import requests
import json


def translateMessage(message="do you want food?"):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": message,
        "target": "es",
        "source": "en"
    }
    headers = {
	    "content-type": "application/x-www-form-urlencoded",
	    "Accept-Encoding": "application/gzip",
	    "X-RapidAPI-Key": "4d7a4b548emsheca51641ea28fcap1897bbjsn7daa98afcafb",
	    "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    firstInd = response.text.find("translatedText")
    temp = response.text.find(":", firstInd + 1)
    secondInd = response.text.find("}", temp + 1)
    print(response.text[temp+2:secondInd-1])
"""
response.text.find(":", firstInd + 1)
"""
translateMessage()

