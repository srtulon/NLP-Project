import pyttsx3

import speech_recognition as sr
import re
import time
import webbrowser


import wikipediaapi as api
import wikipedia as wk

import smtplib
import requests

import urllib.request
import urllib.parse

from bs4 import BeautifulSoup as bs
import requests


import paho.mqtt.publish as publish

engine = pyttsx3.init()
engine.setProperty("rate", 178)


# Wikipediaapi 'initialization'
wiki_wiki = api.Wikipedia('en')






def summary(pg, sentences=5):
    summ = pg.summary.split('. ')
    summ = '. '.join(summ[:sentences])
    summ += '.'
    return summ


  
def calculator(ques):
    # print(type(ques))
    #ques=re.sub("[^0-9+-/*]", "", ques)
    ques=ques.replace(" ","")
    ques=ques.replace("into","*")
    ques=ques.replace("divide","/")
    ques=ques.replace("multiply","*")
    ques=ques.replace("substract","-")
    ques=ques.replace("subtract","-")
    
    try:
        return format(eval(ques),".2f")
    except:
        return "Invalid equation. Please try again"
    
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
    mail.login("xxxxxx@gmail.com", "xxxxxxxxxxxxx")

    # send message
    mail.sendmail("FROM", "TO", content)

    # end mail connection
    mail.close()

    return("Email sent.")



def google(ques):
    
   
    domain = ques.replace(" ","+")
    webbrowser.open("https://www.google.com/search?&q="+domain)
    


# search in wikipedia (e.g. Can you search in wikipedia apples)
def wikipedias(ques):
    
    wk_res = wk.search(ques)
    page = wiki_wiki.page(wk_res[0])
    print("Page summary", summary(page))
    webbrowser.open(page.fullurl)
    return summary(page)
    
    

# Search videos on Youtube and play (e.g. Search in youtube believer)
def youtube(ques):
    
    
    domain = ques.replace(" ","+")
    
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+domain)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    #print(video_ids)
    webbrowser.open("http://www.youtube.com/watch?v={}".format(video_ids[0]))
    
   
        
    
#  weather forecast in your city (e.g. weather in London)
# please create and use your own API it is free
# def weather():
#     city=input('Enter city: ')  
#     url1 = 'https://wttr.in/{}?format=1'.format(city)
#     res1 = requests.get(url1)
#     print(res1.text.decode('utf-8'))
#     # url2 = 'https://wttr.in/{}'.format(city)
#     # res2 = requests.get(url2)
#     # print(res2.text)
    
def weather(city):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    # US english
    LANGUAGE = "en-US,en;q=0.5"
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    import argparse
    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default=city)
    # parse arguments
    args = parser.parse_args()
    region = args.region
    URL += region
    # get data
    
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(URL)
    # create a new soup
    soup = bs(html.text, "html.parser")

    #print(soup)
    #location = soup.select('#wob_loc')[0].getText().strip()
    #time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.find("span", attrs={"id": "wob_dc"}).text
    weather = soup.find("span", attrs={"id": "wob_tm"}).text
    
    return [info,weather]
    
    
def news():
    webbrowser.open('https://www.economist.com/')
    

def onoff(ques):
    
    if 'on' in ques.lower():        
        publish.single("onoff", 1, hostname="192.168.2.13")
        return("Okay! Turning the light on")
    
    if 'off' in ques.lower():
        
        publish.single("onoff", 0, hostname="192.168.2.13")
        
        return("Okay! Turning the light off")