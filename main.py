import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import warnings
import os 
from AppOpener import open as open_app, close as close_app
import pywhatkit as kit
import pyautogui
import time
import requests  # ওয়েদার ফিচারের জন্য

warnings.filterwarnings("ignore")

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- সুপার ফাস্ট কান (মাঝখানে থামলেও পুরো কথা শুনবে) ---
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening (Speak comfortably)...")
        
        listener.energy_threshold = 300  
        listener.dynamic_energy_threshold = False 
        listener.pause_threshold = 3.0   
        
        try:
            audio = listener.listen(source, timeout=10, phrase_time_limit=15)
        except:
            return "none"

        try:
            print("Recognizing...")
            command = listener.recognize_google(audio).lower()                       
            print(f"user said: {command}")
            return command
        except:
            print("Sorry, I did not get that. Please say that again.")
            return "none"

speak("I am ready. Tell me what to do.")
is_music_playing = False

while True:
    my_command = take_command()

    # উইকিপিডিয়া সার্চ
    if 'wikipedia' in my_command:
        speak("Searching Wikipedia...")
        try:
            query = my_command.replace("wikipedia","").strip()
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            speak(results)
        except:
            speak("Sorry, I could not find any information on that.")

    # ইউটিউবে গান/ভিডিও প্লে করা
    elif 'play' in my_command:
        song = my_command.replace('play', '').strip()
        if not song:
            speak("What song should I play?")
            continue
        speak(f"playing {song}")
        
        if is_music_playing == True:
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1)
        try:
            kit.playonyt(song)
            is_music_playing = True
        except:
            speak("Sorry, I could not play that song.")

    # পুরোপুরি ট্যাব কেটে দেওয়া
    elif 'close tab' in my_command or 'close video' in my_command:   
        speak("Closing the tab")
        pyautogui.hotkey('ctrl', 'w')
        is_music_playing = False

    # ভিডিও পজ বা থামানো
    elif 'pause' in my_command or 'stop video' in my_command or 'stop music' in my_command:
        speak("Pausing")
        pyautogui.press('k')

    # পজ করা ভিডিও আবার চালু করা
    elif 'resume' in my_command or 'continue' in my_command or 'start music' in my_command or 'start video' in my_command:
        speak("Resuming")
        pyautogui.press('k')

    # গান চেঞ্জ করা
    elif 'change music' in my_command or 'next song' in my_command or 'next video' in my_command:
        speak("Playing next")
        pyautogui.hotkey('shift', 'n')

    # ভলিউম বাড়ানো/কমানো
    elif 'volume up' in my_command or 'increase volume' in my_command:
        speak("Increasing volume")
        for i in range(5):
            pyautogui.press('volumeup')

    elif 'volume down' in my_command or 'decrease volume' in my_command:
        speak("Decreasing volume")
        for i in range(5):
            pyautogui.press('volumedown')

    # মিউট করা
    elif 'mute' in my_command or 'unmute' in my_command:
        speak("Done")
        pyautogui.press('m')

    # সরাসরি ইউটিউব খোলা
    elif 'youtube' in my_command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    # গুগল সার্চ এবং সরাসরি তথ্য পড়া
    elif 'search' in my_command or 'google search' in my_command:
        query = my_command.replace("google search", "").replace("search", "").replace("on google", "").strip()
        speak(f"Searching for {query}")
        try:
            speak("Here is what I found.")
            result = kit.info(query, lines=2)
            print(result)
            speak(result)
        except:
            speak("Opening Google for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    # ব্রাউজারে Back-এ যাওয়া 
    elif 'go back' in my_command or 'back page' in my_command or 'previous page' in my_command:
        speak("Going back")
        pyautogui.hotkey('alt', 'left')

    # পেজ স্ক্রল করা
    elif 'scroll down' in my_command:
        speak("Scrolling down")
        pyautogui.press('pagedown') 

    elif 'scroll up' in my_command:
        speak("Scrolling up")
        pyautogui.press('pageup')   

    # ডাইনামিক ওয়েবসাইট ওপেনার
    elif 'open website' in my_command:
        website_name = my_command.replace("open website", "").strip()
        speak(f"Opening {website_name}")
        webbrowser.open(f"https://www.{website_name}.com")

    # লিংকে সিলেক্ট করা এবং ঢোকা
    elif 'press enter' in my_command or 'click' in my_command:
        speak("Clicking")
        pyautogui.press('enter')

    elif 'next link' in my_command or 'press tab' in my_command:
        pyautogui.press('tab')

    # স্ক্রিনশট নেওয়া
    elif 'take screenshot' in my_command or 'take a screenshot' in my_command or 'capture screen' in my_command:
        speak("Taking screenshot")
        time_string = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{time_string}.png"
        try:
            img = pyautogui.screenshot()
            img.save(file_name)
            speak("Screenshot saved successfully")
        except:
            speak("Sorry, I could not take the screenshot.")

    # পিসির যেকোনো অ্যাপ খোলা
    elif 'open' in my_command:
        app_name = my_command.replace("open", "").strip()
        speak(f"opening {app_name}")
        try:
            open_app(app_name, match_closest=True)
        except:
            speak(f"Sorry, I could not find {app_name} in your PC.")
            
    # পিসির যেকোনো অ্যাপ বন্ধ করা
    elif 'close app' in my_command:
        app_name = my_command.replace("close app", "").strip()
        speak(f"Closing {app_name}")
        try:
            close_app(app_name, match_closest=True)
        except:
            speak(f"Sorry, I could not close {app_name}.")

    # --- আপডেট ম্যাজিক: মানুষের মতো কিবোর্ডে টাইপ করা (ক্যালকুলেটরের জন্য) ---
    elif 'type' in my_command or 'press' in my_command or 'write' in my_command:
        math_keys = my_command.replace("type", "").replace("press", "").replace("write", "").strip()
        math_keys = math_keys.replace("plus", "+").replace("minus", "-").replace("multiplied by", "*").replace("into", "*").replace("x", "*").replace("divided by", "/").replace("equal", "=").replace("equals", "=")
        math_keys = math_keys.replace(" ", "")
        
        speak("Typing")
        if '=' in math_keys:
            clean_keys = math_keys.replace("=", "")
            pyautogui.write(clean_keys, interval=0.1) 
            pyautogui.press('enter') 
        else:
            pyautogui.write(math_keys, interval=0.1)
                
    # ভুল হলে একটা সংখ্যা কাটা (Backspace)
    elif 'delete' in my_command or 'backspace' in my_command:
        speak("Deleting")
        pyautogui.press('backspace')
        
    # পুরো ক্যালকুলেটর জিরো (0) করে দেওয়া
    elif 'clear all' in my_command or 'clear screen' in my_command:
        speak("Clearing")
        pyautogui.press('esc') 

    # --- নতুন ম্যাজিক: আবহাওয়া বা টেম্পারেচার জানা ---
    elif 'weather' in my_command or 'temperature' in my_command:
        city = "Dhaka" 
        if 'in' in my_command:
            city = my_command.split('in')[-1].strip()
            
        speak(f"Checking weather for {city}")
        
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_response = requests.get(geo_url).json()
            
            if "results" in geo_response:
                lat = geo_response["results"][0]["latitude"]
                lon = geo_response["results"][0]["longitude"]
                
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = requests.get(weather_url).json()
                
                temp = weather_response["current_weather"]["temperature"]
                wind = weather_response["current_weather"]["windspeed"]
                
                result = f"The current temperature in {city} is {temp} degree Celsius with a wind speed of {wind} kilometers per hour."
                print(result)
                speak(result)
            else:
                speak(f"Sorry, I could not find the location {city}.")
        except:
            speak("Sorry, I could not fetch the weather details right now.")

    # সময় জানা
    elif 'time' in my_command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")
        print(f"Time: {current_time}")

    # প্রোগ্রাম বন্ধ করা
    elif 'exit' in my_command or 'goodbye' in my_command or 'go to sleep' in my_command:
        speak("Goodbye!")
        break

    elif my_command != "none":
        speak("I don't know how to do that yet.")