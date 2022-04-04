import pyttsx3

import speech_recognition as sr
import re
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


import wikipediaapi as api
import wikipedia as wk

import smtplib
import requests

import urllib.request
import urllib.parse
import json
import bs4

import paho.mqtt.publish as publish

engine = pyttsx3.init()
engine.setProperty("rate", 178)

#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Wikipediaapi 'initialization'
wiki_wiki = api.Wikipedia('en')

# b = firefox_binary=FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\')

# dr = webdriver.Firefox(firefox_binary=b)

# ff_Binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
# driver = webdriver.Firefox(firefox_binary = ff_Binary)

#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
#s=Service(ChromeDriverManager().install())
#driver = webdriver.Chrome()


def myCommand():
    "listens for commands"
    # Initialize the recognizer
    # The primary purpose of a Recognizer instance is, of course, to recognize speech.
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ready...")
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        # listens for the user's input
        audio = r.listen(source)
        print("analyzing...")

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        time.sleep(2)
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print("Your last command couldn't be heard")
        command = myCommand()

    return command

def talk(val):
    print(val)
    engine.say(val)
    engine.runAndWait()


def summary(pg, sentences=5):
    summ = pg.summary.split('. ')
    summ = '. '.join(summ[:sentences])
    summ += '.'
    return summ


  
def calculator(ques):
    ques=re.sub("[^0-9+-/*]", "", ques)
    try:
        print(format(eval(ques),".2f"))
    except:
        print("Invalid equation. Please try again")
    
def email():
        
    engine.say("What is the subject?")
    engine.runAndWait()
    subject = myCommand()
    engine.say("What should I say?")
    engine.runAndWait()
    message = myCommand()
    content = "Subject: {}\n\n{}".format(subject, message)

    # init gmail SMTP
    mail = smtplib.SMTP("smtp.gmail.com", 587)

    # identify to server
    mail.ehlo()

    # encrypt session
    mail.starttls()

    # login
    mail.login("srtulon6@gmail.com", "Bmwm3gtrxz5")

    # send message
    mail.sendmail("FROM", "TO", content)

    # end mail connection
    mail.close()

    talk("Email sent.")



def google(ques):
    
    talk("What do you want to search?")    
    domain = myCommand().replace(" ","+")
    webbrowser.open("https://www.google.com/search?&q="+domain)


# search in wikipedia (e.g. Can you search in wikipedia apples)
def wikipedia(ques):
    talk("What do you want to search?")
    domain = myCommand()
    wk_res = wk.search(domain)
    page = wiki_wiki.page(wk_res[0])
    print("Page summary", summary(page))
    webbrowser.open(page.fullurl)
    

# Search videos on Youtube and play (e.g. Search in youtube believer)
def youtube(ques):
    talk("What do you want to play?")
    
    domain = myCommand().replace(" ","+")
    
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+domain)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    #print(video_ids)
    webbrowser.open("http://www.youtube.com/watch?v={}".format(video_ids[0]))
        
    
#  weather forecast in your city (e.g. weather in London)
# please create and use your own API it is free
def weather():
    city=input('Enter city: ')  
    url1 = 'https://wttr.in/{}?format=1'.format(city)
    res1 = requests.get(url1)
    print(res1.text.decode('utf-8'))
    # url2 = 'https://wttr.in/{}'.format(city)
    # res2 = requests.get(url2)
    # print(res2.text)
    
def news():
    webbrowser.open('https://www.economist.com/')
    

def onoff(ques):
    
    if 'on' in ques:
        talk("Okay! Turning the light on")
        
        publish.single("onoff", 1, hostname="192.168.2.13")
    
    if 'off' in ques:
        talk("Okay! Turning the light off")
        publish.single("onoff", 0, hostname="192.168.2.13")