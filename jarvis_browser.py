import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import platform
import shutil
from urllib.parse import quote_plus

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen from microphone and return recognized command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"🗣️ You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return ""

def find_chrome_path():
    """Detect Google Chrome installation path."""
    system = platform.system()
    if system == "Windows":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in paths:
            if shutil.os.path.exists(path):
                return path
    elif system == "Darwin":  # macOS
        path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if shutil.os.path.exists(path):
            return path
    else:  # Linux
        path = shutil.which("google-chrome") or shutil.which("chromium")
        return path
    return None

def open_chrome():
    """Open Google Chrome browser."""
    path = find_chrome_path()
    speak("Opening Google Chrome.")
    if path:
        subprocess.Popen([path])
    else:
        webbrowser.open("https://www.google.com")

def search_google(query):
    """Perform Google search."""
    url = "https://www.google.com/search?q=" + quote_plus(query)
    path = find_chrome_path()
    speak(f"Searching Google for {query}")
    if path:
        subprocess.Popen([path, url])
    else:
        webbrowser.open(url)

def open_website(site_name):
    """Try to open any website by name."""
    site_name = site_name.replace("open", "").replace("website", "").strip()
    if not site_name:
        speak("Please tell me which website to open.")
        return
    if "." not in site_name:
        # If user said “open YouTube”, add .com
        site_name = site_name.replace(" ", "")
        url = f"https://www.{site_name}.com"
    else:
        url = f"https://{site_name}"
    speak(f"Opening {site_name}")
    path = find_chrome_path()
    if path:
        subprocess.Popen([path, url])
    else:
        webbrowser.open(url)

def main():
    speak("Hello, I am Jarvis. How can I assist you?")
    while True:
        command = listen()

        if "open chrome" in command:
            open_chrome()

        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                search_google(query)
            else:
                speak("What should I search for?")
                query = listen()
                if query:
                    search_google(query)

        elif "open" in command:
            open_website(command)

        elif any(word in command for word in ["exit", "quit", "stop"]):
            speak("Goodbye!")
            break

        elif command:
            speak("Sorry, I can open Chrome, search Google, or open websites right now.")

if __name__ == "__main__":
    main()


