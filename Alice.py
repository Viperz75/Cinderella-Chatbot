import datetime
import operator
import os
import random
import sys
import time
import webbrowser

import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import randfacts
import requests
import speech_recognition as sr
import wikipedia
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
from requests import get

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 180)


# Text to Speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Voice to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"You: {query}\n")

    except Exception as e:
        return "none"
    query = query.lower()
    return query


# News
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=google-news&apiKey=7fd4c0e6cfd649e99e7639e90ac8cbab'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"Today's {day[i]} news is: {head[i]}")


# Zodiac Calculator
def zodiac():
    speak("What month were you born?")
    month = takecommand().lower()
    speak("What day were you born?")
    day = int(takecommand().lower())
    months = ["march", "april", "may", "june", "july", "september", "august", "november", "october", "december",
              "january", "february"]
    if month in months:
        sign = ""
        if month == "march":
            sign = "Pisces" if (day < 21) else "Aries"
        elif month == "april":
            sign = "Aries" if (day < 20) else "Taurus"
        elif month == "may":
            sign = "Taurus" if (day < 20) else "Gemini"
        elif month == "june":
            sign = "Gemini" if (day < 20) else "Cancer"
        elif month == "july":
            sign = "Cancer" if (day < 20) else "Leo"
        elif month == "august":
            sign = "Leo" if (day < 20) else "Virgo"
        elif month == "september":
            sign = "Virgo" if (day < 20) else "Libra"
        elif month == "october":
            sign = "Libra" if (day < 20) else "Scorpio"
        elif month == "november":
            sign = "Scorpio" if (day < 20) else "Sagittarius"
        elif month == "december":
            sign = "Sagittarius" if (day < 20) else "Capricorn"
        elif month == "january":
            sign = "Capricorn" if (day < 20) else "Aquarius"
        elif month == "february":
            sign = "Aquarius" if (day < 20) else "Pisces"
        speak("You Zodiac Sign is " + sign)


# Temperature
def temperature():
    search = "temperature"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp} outside")


# Location
def location():
    speak("Checking Location")
    try:
        ipAdd = requests.get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        speak(f"I am not sure but i think we are in {city}. City of {country}.")
    except Exception as e:
        speak("Sorry, Due to network issue i am not able to find our location.")
        pass


# Wish_Function
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Hello, I am Alice. How may i help you?")


def TaskExecution():
    wish()
    while True:
        query = takecommand()

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<Logic Building to perform tasks>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        date = datetime.datetime.today().strftime("%I:%M %p")

        if "time now" in query:
            speak("The time is now " + date + "")

        elif 'joke' in query or 'funny' in query:
            speak(pyjokes.get_joke())

        elif 'open google' in query or 'search in google' in query:
            speak("What should i search on Google")
            google = takecommand().lower()
            webbrowser.open(f'www.google.com/search?q=' + google)
            speak("Searching in google...")

        elif 'open bing' in query or 'search in bing' in query:
            speak("What should i search on Bing")
            bing = takecommand().lower()
            webbrowser.open(f'www.bing.com/search?q=' + bing)
            speak("Searching in Bing...")

        elif 'open duckduckgo' in query or 'search in duckduckgo' in query:
            speak("What should i search on DuckDuckGo")
            duck = takecommand().lower()
            webbrowser.open(f'www.duckduckgo.com/search?q=' + duck)
            speak("Searching in DuckDuckGo...")

        elif 'open youtube' in query:
            speak("What do you want me to play")
            youtube = takecommand().lower()
            pywhatkit.playonyt(youtube)
            speak("Playing...")

        elif "my ip" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your ip address is {ip}")

        elif 'open wikipedia' in query:
            speak("What do you want to know from Wikipedia?")
            wiki = takecommand().lower()
            info = wikipedia.summary(wiki, 2)
            speak("According to Wikipedia")
            speak(info)

        elif "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif "open cmd" in query:
            os.system("start cmd")

        elif 'open task manager' in query:
            tpath = "C:\\Windows\\system32\\Taskmgr.exe"
            os.startfile(tpath)

        elif "open steam" in query:
            spath = "C:\\Program Files (x86)\\Steam\\steam.exe"
            os.startfile(spath)

        elif "open epic games" in query:
            epath = "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe"
            os.startfile(epath)

        elif "open browser" in query:
            bpath = "C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe"
            os.startfile(bpath)
            speak("Opening Edge...")

        elif 'developer' in query or 'made you' in query:
            speak("My Developer is Niaz Mahmud Akash and Jalish Mahmud Sujon")

        elif 'thanks' in query or 'thank you' in query or 'thanks a lot' in query:
            thanks = ["Glad to help you.", "Happy to help", "You're welcome"]
            thanks_random = random.choice(thanks)
            speak(thanks_random)

        elif 'browser' in query:
            webbrowser.open_new('www.google.com')
            speak("Opening Browser...")

        elif 'open facebook' in query:
            webbrowser.open('www.facebook.com')
            speak("Opening Facebook...")

        elif 'open twitter' in query:
            webbrowser.open('www.twitter.com')
            speak("Opening Twitter...")

        elif 'open telegram' in query:
            webbrowser.open('https://web.telegram.org/')
            speak("Opening Telegram...")

        elif 'open youtube' in query:
            webbrowser.open('www.youtube.com')
            speak("Opening Youtube...")

        elif 'open play store' in query:
            webbrowser.open('https://play.google.com/store/apps')
            speak("Opening Google PlayStore...")

        elif 'open instagram' in query:
            webbrowser.open('www.instagram.com')
            speak("Opening Instagram...")

        elif 'love me' in query:
            love = ["Of course. You're one of a kind.", "Is that a thing to ask? Of course I LOVE YOU ❤",
                    "Yes, in an at-your-service sor of way"]
            love_random = random.choice(love)
            speak(love_random)

        elif 'i love you' in query:
            express = ["That's so amazing to hear", "I LOVE ME Too!", "If I was you, I'd love me too.",
                       "Of course you do! Friends don't hate each other."]
            express_random = random.choice(express)
            speak(express_random)

        elif 'will you go on a' in query:
            go = ["Sure. Just let me know the place and time", "I'd go anywhere you take me"]
            go_random = random.choice(go)
            speak(go_random)

        elif 'you robot' in query or 'are you human' in query:
            speak("Yes, I am a Robot but a smart one. Let me prove it to you. How can i help you?")

        elif 'your name' in query:
            speak("My name is Alice. I am your virtual personal assistant.")

        elif 'how are you' in query or 'hows things' in query or 'how you doing' in query:
            how = ["I am fine. What about you?", "I am good. How are you?"]
            how_random = random.choice(how)
            speak(how_random)

        elif 'marry me' in query:
            marry = [
                "This is one of those things we both have to agree on. I'd prefer to keep our relationship friendly. Romance makes me incredibly awkward",
                "It's not possible"]
            marry_random = random.choice(marry)
            speak(marry_random)

        elif 'about nidhi' in query:
            speak("She can suck my pussy")

        elif 'happy' and 'valentines' in query:
            speak("Happy Valentines Day.")

        elif 'mothers name' in query or 'your mother' in query:
            mname = ["I have no mother. I am an Ai", "Every user is my family",
                     "It takes a village to raise a virtual assistant"]
            mname_random = random.choice(mname)
            speak(mname_random)

        elif 'your boss' in query:
            speak("You are")

        elif 'where am' in query or 'location' in query or 'where are we' in query:
            location()

        elif 'take a screenshot' in query or 'screenshot' in query:
            speak('What should be the name of this screenshot?')
            name = takecommand().lower()
            speak('Taking Screenshot')
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak('Screenshot Saved')

        elif 'fact' in query or 'facts' in query:
            x = randfacts.getFact()
            speak(x)

        elif 'annoying' in query or 'you suck' in query:
            dtalk = ["I am sorry", "You can report about me in GitHub", "Sorry, i am just an ai"]
            dtalk_random = random.choice(dtalk)
            speak(dtalk_random)

        elif 'youre cute' in query or 'smart' in query or 'you are cute' in query or 'you are creepy' in query:
            cute = ["Thank you", "Thanks", "Thanks, that means a lot", "Much obliged!", "Well, that makes two of us!"]
            cute_random = random.choice(cute)
            speak(cute_random)

        elif 'you live' in query or 'your home' in query:
            live = ["I live in your computer", "I live in a place filled with games", "I live in Servers of Github",
                    "I live in the internet"]
            live_random = random.choice(live)
            speak(live_random)

        elif 'news' in query:
            speak("Sure. Getting News...")
            news()

        elif 'system' and 'report' in query or 'system' and 'status' in query:
            battery = psutil.sensors_battery()
            cpu = psutil.cpu_percent(interval=None)
            percentage = battery.percent
            speak(f"All Systems are running. Cpu usage is at {cpu} percent. We have {percentage} percent battery.")

        elif 'like me' in query:
            like = ["Yes, I like you", "I like you well enough so far", "Of Course", "I don't hate you"]
            like_random = random.choice(like)
            speak(like_random)

        elif 'what are you doing' in query or 'thinking' in query:
            think = ["Thinking about my future", "I am trying to figure out what came first? Chicken or egg.",
                     "Algebra",
                     "I plan on waiting here quietly until someone asks me a question"]
            think_random = random.choice(think)
            speak(think_random)

        elif 'about me' in query:
            speak("You're Intelligent and ambitious")

        elif 'dictionary' in query:
            speak("Dictionary Opened")
            while True:
                dinput = takecommand()
                try:
                    if 'close' in dinput or 'exit' in dinput:
                        speak("Dictionary Closed")
                        break
                    else:
                        dictionary = PyDictionary(dinput)
                        speak(dictionary.getMeanings())

                except Exception as e:
                    speak("Sorry, I am not able to find this.")

        elif 'date' in query or 'day' in query:
            x = datetime.datetime.today().strftime("%A %d %B %Y")
            speak(x)

        elif 'zodiac' in query:
            zodiac()

        elif 'horoscope' in query:
            speak("Do you know your Zodiac Sign?")
            z = takecommand().lower()
            if 'no' in z:
                zodiac()
            elif 'yes' in z or 'yeah' in z:
                speak("What is your Zodiac Sign?")
                sign = takecommand()
                speak("Do you want to know the horoscope of today, tomorrow or yesterday?")
                day = takecommand()
                params = (
                    ('sign', sign),
                    ('day', day)
                )
                response = requests.post('https://aztro.sameerkumar.website/', params=params)
                json = response.json()
                print("Horoscope for", json.get('current_date'), "\n")
                speak(json.get('description'))
                print('\nCompatibility:', json.get('compatibility'))
                print('Mood:', json.get('mood'))
                print('Color:', json.get('color'))
                print('Lucky Number:', json.get('lucky_number'))
                print('Lucky Time:', json.get('lucky_time'), "\n")

        # How to Do Mode
        elif 'activate how to' in query:
            speak("How to mode is activated.")
            while True:
                speak("Please tell me what do you want to know?")
                how = takecommand()
                try:
                    if 'exit' in how or 'close' in how:
                        speak("How to do mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry. I am not able to find this")

        elif 'temperature' in query or 'weather today' in query:
            temperature()

        # Little Chitchat
        elif 'hello' in query or 'hi' in query or 'hey' in query:
            speak("Hello, How are you doing?")
            reply = takecommand().lower()

            if 'what' and 'about' and 'you' in reply:
                how2 = ["I am fine.", "I am good."]
                how2_random = random.choice(how2)
                speak(how2_random)

            elif 'not good' in reply or 'bad' in reply or 'terrible' in reply:
                speak("I am sorry to hear that. Everything will be okay.")

            elif 'great' in reply or 'good' in reply or 'excellent' in reply or 'fine' in reply:
                speak("That's great to hear from you.")

        elif 'help' in query or 'what can you do' in query or 'how does it work' in query:
            do = ["I can tell you Time", "Joke", "Open browser", "Open Youtube/Facebook/Twitter/Telegram/Instagram",
                  "Open or Close applications", "Search in Wikipedia", "Play videos in Youtube",
                  "Search in Google/Bing/DuckDuckGo", "I can calculate", "Learn how to make or do something.",
                  "Switch Window", "Play news", "Tell you about interesting facts",
                  "Temperature of you current location", "Can take Screenshot", "Can find your location",
                  "Shutdown/Restart Computer", "Horoscope", "Dictionary", "Zodiac Sign Calculator", "System Report"]
            for does in do:
                speak(does)

        elif 'introduce yourself' in query or 'who are you' in query:
            speak(
                "I am Alice. Your personal virtual Assistant. Developed by Jalish Mahmud Sujon and Niaz Mahmud Akash in 2021.")

        elif 'go to sleep' in query:
            speak("Sleep mode activated. If you need me just say Wake up.")
            break

        elif 'goodbye' in query:
            speak("Good bye. Have a Lovely day.")
            sys.exit()

        # To close Applications
        elif 'shutdown' in query:
            speak("Shutting Down")
            os.system("shutdown /s /t 5")
            sys.exit()

        elif 'restart' in query:
            speak("Restarting Computer")
            os.system("shutdown /r /t 5")
            sys.exit()

        elif "close notepad" in query:
            speak("Closing Notepad")
            os.system("taskkill /f /im notepad.exe")

        elif "close browser" in query:
            speak("Closing Browser")
            os.system("taskkill /f /im edge.exe")

        elif "close steam" in query:
            speak("Closing Steam")
            os.system("taskkill /f /im steam.exe")

        elif "close epic games" in query:
            speak("Closing Epic Games")
            os.system("taskkill /f /im EpicGamesLauncher.exe")

        elif 'close task manager' in query:
            speak("Closing Task Manager")
            os.system("taskkill /f /im Taskmgr.exe")

        # Switch Window
        elif 'switch window' in query or 'switch the windows' in query or 'switch windows' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Calculator Function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        elif 'do some calculations' in query or 'calculate' in query or 'open calculator' in query:
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("What you want to calculate? Example 6 plus 6")
                    print("listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,  # Plus
                        '-': operator.sub,  # Minus
                        'x': operator.mul,  # Multiplied by
                        'divided by': operator.__truediv__,  # Divided by
                    }[op]

                def eval_binary_expr(op1, oper, op2):  # 5 plus 8
                    op1, op2 = float(op1), float(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak("Your Result is")
                speak(eval_binary_expr(*(my_string.split())))

            except Exception:
                speak("Sorry i didn't catch that. Please try again")


if __name__ == "__main__":
    while True:
        permission = takecommand()
        if 'wake up' in permission or 'wakeup' in permission or 'alice' in permission:
            TaskExecution()
        elif 'goodbye' in permission or 'good bye' in permission:
            speak("Thanks for letting me help. Have a lovely day.")
            sys.exit()
