
from tkinter import *
import tkinter
from PIL import ImageTk, Image
import random


# import skills
from skills import *

# import intent detection and slot filling
from nlu import *



engine = pyttsx3.init()
engine.setProperty("rate", 178)

lang = "en"

check=True


import json
with open('responses.json') as json_data:
    responses = json.load(json_data)

#print(type(responses))

def response(sentence):
    results = classify(sentence)
    
    #print(type(results[0]))
    if len(results[0])<1:
        results[0]=='oos'
        
    for i in responses['responses']:
        if i['tag'] == results[0]:
            if len (i['responses'])>0:
                val = random.choice(i['responses'])
                if len(results[1])>0:
                    val=val+results[1]
                talk(val)
           
    return results

def myCommand():
    "listens for commands"
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        # listens for the user's input
        audio = r.listen(source)
        print("analyzing...")

    try:
        command = r.recognize_google(audio).lower()
        msg_list.insert(tkinter.END,"")
        msg_list.insert(tkinter.END,"   You : "+command)
        msg_list.see(tkinter.END)

    except sr.UnknownValueError:
        talk(random.choice(["Sorry, can't understand you", "Please give me more info", "Not sure I understand"]))
        command = ""

    return command

def talk(val):
    msg_list.insert(tkinter.END,"")
    msg_list.insert(tkinter.END,"   Assistant : "+val)
    msg_list.see(tkinter.END)
    engine.say(val)
    engine.runAndWait()
            




def call():
    
    # if check:
    #     talk("Hi I am your personal assistant, ask me something!")
    #     check=False
    
    ques = myCommand()
    
    if ques == 'close':
        talk("Good bye")
        pass
    
    
    ques2=response(ques)

    
    if 'wikipedia' in ques2:
        data=wikipedias(ques2[1])
        # msg_list.insert(tkinter.END,"")
        # msg_list.insert(tkinter.END,"   Assistant : "+data)
        # msg_list.see(tkinter.END)

    if'news' in ques2:
        news()

    if 'google' in ques2:
        google(ques2[1])

    if 'calculate' in ques2:
       talk(calculator(ques2[1]))
    
    if 'youtube' in ques2:
       youtube(ques2[1])
       
    if 'weather' in ques2:
       data=weather(ques2[1])
       talk("The weather is "+data[0])
       talk("And the temperature is "+data[1]+"°C")
    
    if 'turnLightOn' in ques2 or 'turnLightOff' in ques2:
       talk(onoff(ques2[0]))



top = tkinter.Tk()
top.configure(background="white")
top.title("Assistant")
messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame,highlightthickness = 0, bd = 0, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
img1=ImageTk.PhotoImage(Image.open("voice.png"))
send_button = tkinter.Button(top,highlightthickness = 0, bd = 0,bg="white",image=img1, text="Send",command=call)
send_button.pack(side=TOP, padx=10, pady=20)

tkinter.mainloop()   
    