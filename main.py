import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary
from openai import OpenAI
import os

# ------------------ INITIAL SETUP -----------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()

NEWS_API_KEY = "1fa8eae6eab84ffead8d531168a2718a"
OPENAI_API_KEY = "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"


# ------------------ SPEAK FUNCTION ------------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------ AI PROCESS ------------------
def aiProcess(command):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa."
            },
            {"role": "user", "content": command}
        ]
    )

    return response.choices[0].message.content

# ------------------ COMMAND PROCESSOR ------------------
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open whatsapp" in c:
        webbrowser.open("https://whatsapp.com")

    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in c:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        )

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles[:5]:
                speak(article["title"])
        else:
            speak("Unable to fetch news")

    else:
        output = aiProcess(c)
        speak(output)

# ------------------ MAIN LOOP ------------------
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=20, phrase_time_limit=2)

            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yahhh....")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
