import sys
import time
import pyaudiowpatch as pyaudio
from datetime import datetime
import webbrowser
import smtplib
import requests
API_KEY = ""
knowledge = {
    "what is python": "Python is a high-level programming language used for software development, automation, data science, and many other applications.",
    "what is artificial intelligence": "Artificial intelligence is the ability of computers to perform tasks that normally require human intelligence."
}
custom_commands = {
    "open my project": "Opening your project.",
    "good morning": "Good morning! Have a great day."
}

sys.modules["pyaudio"] = pyaudio

import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
def set_reminder(seconds):
    speak("Reminder set.")
    time.sleep(seconds)
    speak("your reminder is due.")
def send_email():
    sender_email = "your_@gemail.com"
    receiver_email ="your_@gmail.com"
    app_password = ""

    message = "Hello! This is a test email from my Voice Assistant."

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message)

    speak("Email sent successfully.")
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Sorry, I could not find the weather for that location.")
    
while True:
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
        print("Audio captured")

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        command_found=False
        command = text.lower()
        if "hello" in command:
            command_found = True
            speak("Hello! How can I help you?")

        elif "time" in command and "date" in command:
            command_found = True
            current_time = datetime.now().strftime("%I:%M %p")
            today = datetime.now().strftime("%B %d, %Y")
            speak("Today's date is " + today + " and the current time is " + current_time)
        elif "time" in command:
            print("TIME COMMAND FOUND")
            command_found = True
            current_time = datetime.now().strftime("%I:%M %p")
            print("CURRENT TIME:",current_time)
            print("Speaking time now...")
            speak("The current time is " + current_time)
            print("Finished speaking")

        elif "date" in command:
            command_found = True
            today = datetime.now().strftime("%B %d, %Y")
            speak("Today's date is " + today)

        elif "send email" in command:
            command_found = True
            send_email()
        elif "reminder" in command:
            command_found = True
            words = command.split()

            for word in words:
                if word.isdigit():
                    seconds = int(word)
                    set_reminder(seconds)
                    break
        elif "weather" in command or "temperature" in command or "forecast" in command:
            command_found = True
            get_weather("Chennai")
            command_found = True
        

        elif "artificial intelligence" in command or "ai" in command:
            command_found = True
            speak(knowledge["what is artificial intelligence"])
        elif command in custom_commands:
            command_found = True
            speak(custom_commands[command])
        elif "search" in command:
            command_found = True
            search_query = command.replace("search", "").strip()
            webbrowser.open("https://www.google.com/search?q=" + search_query)
            speak("Here are the search results.")

        elif "python" in command:
            command_found = True
            speak(knowledge["what is python"])

        if not command_found:
            print("Command not recognized:", command)
    except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please say that again.")

    except sr.RequestError:
            speak("Sorry, the speech service is unavailable.")

    except Exception as e:
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR MESSAGE:", repr(e))