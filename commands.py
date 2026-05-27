import os
import cv2
import json
import psutil
import pyjokes
import wikipedia
import pyautogui
import webbrowser
import pywhatkit
import ollama

from datetime import datetime


# =========================================
# MEMORY FILE
# =========================================

MEMORY_FILE = "memory.json"


# =========================================
# SAVE MEMORY
# =========================================


def save_memory(key, value):

    data = {}

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:
            data = json.load(file)

    data[key] = value

    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


# =========================================
# LOAD MEMORY
# =========================================


def load_memory(key):

    if not os.path.exists(MEMORY_FILE):
        return None

    with open(MEMORY_FILE, "r") as file:
        data = json.load(file)

    return data.get(key)


# =========================================
# CAMERA AI
# =========================================


def vision_ai(speak):

    try:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            speak("Camera not found")
            return

        ret, frame = cap.read()

        if not ret:
            speak("Failed to capture image")
            return

        image_path = "vision.jpg"

        cv2.imwrite(image_path, frame)

        cap.release()

        speak("Analyzing camera")

        response = ollama.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": "Describe this image in detail",
                    "images": [image_path]
                }
            ]
        )

        result = response["message"]["content"]

        speak(result)

    except Exception as e:

        print(e)

        speak("Vision system error")


# =========================================
# SCREEN AI
# =========================================


def screen_ai(speak):

    try:

        screenshot = pyautogui.screenshot()

        screenshot.save("screen.jpg")

        speak("Analyzing screen")

        response = ollama.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": "Describe this screen",
                    "images": ["screen.jpg"]
                }
            ]
        )

        result = response["message"]["content"]

        speak(result)

    except Exception as e:

        print(e)

        speak("Screen analysis failed")


# =========================================
# SYSTEM INFO
# =========================================


def system_info(speak):

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    battery = psutil.sensors_battery()

    if battery:
        battery_percent = battery.percent
    else:
        battery_percent = "Unknown"

    speak(
        f"CPU usage is {cpu} percent. "
        f"RAM usage is {ram} percent. "
        f"Battery is {battery_percent} percent"
    )


# =========================================
# APP PATHS
# =========================================

APP_PATHS = {

    "vscode": r"C:\Users\hp\AppData\Local\Programs\Microsoft VS Code\Code.exe",

    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    "spotify": r"C:\Users\hp\AppData\Roaming\Spotify\Spotify.exe",

}


# =========================================
# OPEN APPS
# =========================================


def open_app(app_name, speak):

    try:

        path = APP_PATHS.get(app_name)

        if path and os.path.exists(path):

            os.startfile(path)

            speak(f"Opening {app_name}")

        else:

            speak(f"{app_name} path not found")

    except Exception as e:

        print(e)

        speak("Unable to open app")


# =========================================
# SINGLE COMMAND EXECUTION
# =========================================


def execute_single_command(text, speak):

    text = text.lower().strip()

    # =====================================
    # YOUTUBE
    # =====================================

    if "open youtube" in text:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

        return True
    # =====================================
    # PLAY SONG
    # =====================================

    elif "play" in text:

        song = text.lower()

        remove_words = [
            "jarvis",
            "play",
            "on youtube",
            "youtube",
            "song",
            "music"
        ]

        for word in remove_words:

            song = song.replace(word, "")

        song = song.strip()

        if not song:

            speak("Which song should I play")

            return True

        speak(f"Playing {song}")

        pywhatkit.playonyt(song)

        return True
    # =====================================
    # GOOGLE SEARCH
    # =====================================

    elif "search" in text:

        query = text.replace("search", "").strip()

        speak(f"Searching {query}")

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        return True

    # =====================================
    # OPEN WEBSITES
    # =====================================

    elif "open google" in text:

        speak("Opening Google")

        webbrowser.open("https://google.com")

        return True

    elif "open instagram" in text:

        speak("Opening Instagram")

        webbrowser.open("https://instagram.com")

        return True

    elif "open github" in text:

        speak("Opening GitHub")

        webbrowser.open("https://github.com")

        return True

    elif "open whatsapp" in text:

        speak("Opening WhatsApp")

        webbrowser.open("https://web.whatsapp.com")

        return True

    elif "open chatgpt" in text:

        speak("Opening ChatGPT")

        webbrowser.open("https://chat.openai.com")

        return True

    # =====================================
    # TIME AND DATE
    # =====================================

    elif "time" in text:

        current_time = datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

        return True

    elif "date" in text:

        current_date = datetime.now().strftime("%d %B %Y")

        speak(f"Today's date is {current_date}")

        return True

    # =====================================
    # SCREENSHOT
    # =====================================

    elif "screenshot" in text:

        screenshot = pyautogui.screenshot()

        screenshot.save("screenshot.png")

        speak("Screenshot saved")

        return True

    # =====================================
    # SCREEN AI
    # =====================================

    elif (
        "analyze screen" in text
        or "screen analysis" in text
        or "screen" in text
    ):

        screen_ai(speak)

        return True

    # =====================================
    # CAMERA AI
    # =====================================

    elif (
        "vision" in text
        or "camera" in text
        or "what do you see" in text
    ):

        vision_ai(speak)

        return True

    # =====================================
    # VOLUME CONTROL
    # =====================================

    elif "volume up" in text:

        pyautogui.press("volumeup")

        speak("Volume increased")

        return True

    elif "volume down" in text:

        pyautogui.press("volumedown")

        speak("Volume decreased")

        return True

    elif "mute" in text:

        pyautogui.press("volumemute")

        speak("Muted")

        return True

    # =====================================
    # WINDOW CONTROL
    # =====================================

    elif "close window" in text:

        pyautogui.hotkey("alt", "f4")

        speak("Window closed")

        return True

    elif "switch window" in text:

        pyautogui.hotkey("alt", "tab")

        speak("Switching window")

        return True

    elif "minimize" in text:

        pyautogui.hotkey("win", "down")

        speak("Window minimized")

        return True

    # =====================================
    # TYPE TEXT
    # =====================================

    elif text.startswith("type"):

        typing_text = text.replace("type", "").strip()

        pyautogui.write(typing_text, interval=0.03)

        speak("Typing completed")

        return True

    # =====================================
    # SCROLL
    # =====================================

    elif "scroll down" in text:

        pyautogui.scroll(-1000)

        speak("Scrolling down")

        return True

    elif "scroll up" in text:

        pyautogui.scroll(1000)

        speak("Scrolling up")

        return True

    # =====================================
    # YOUTUBE CONTROLS
    # =====================================

    elif "pause video" in text:

        pyautogui.press("space")

        speak("Video paused")

        return True

    elif "play video" in text:

        pyautogui.press("space")

        speak("Playing video")

        return True

    elif "full screen" in text:

        pyautogui.press("f")

        speak("Fullscreen enabled")

        return True

    # =====================================
    # SYSTEM CONTROL
    # =====================================

    elif "shutdown pc" in text:

        speak("Shutting down computer")

        os.system("shutdown /s /t 5")

        return True

    elif "restart pc" in text:

        speak("Restarting computer")

        os.system("shutdown /r /t 5")

        return True

    # =====================================
    # WINDOWS APPS
    # =====================================

    elif "open notepad" in text:

        speak("Opening Notepad")

        os.system("notepad")

        return True

    elif "open calculator" in text:

        speak("Opening Calculator")

        os.system("calc")

        return True

    elif "open command prompt" in text:

        speak("Opening command prompt")

        os.system("start cmd")

        return True

    elif "open file explorer" in text:

        speak("Opening File Explorer")

        os.system("explorer")

        return True

    # =====================================
    # CUSTOM APPS
    # =====================================

    elif "open vscode" in text:

        open_app("vscode", speak)

        return True

    elif "open chrome" in text:

        open_app("chrome", speak)

        return True

    elif "open spotify" in text:

        open_app("spotify", speak)

        return True

    # =====================================
    # MEMORY SYSTEM
    # =====================================

    elif "my name is" in text:

        name = text.replace("my name is", "").strip()

        save_memory("username", name)

        speak(f"Okay I will remember your name is {name}")

        return True

    elif "what is my name" in text:

        name = load_memory("username")

        if name:
            speak(f"Your name is {name}")
        else:
            speak("I do not know your name yet")

        return True

    # =====================================
    # JOKES
    # =====================================

    elif "tell me a joke" in text:

        joke = pyjokes.get_joke()

        speak(joke)

        return True

    # =====================================
    # WIKIPEDIA
    # =====================================

    elif "who is" in text:

        person = text.replace("who is", "")

        try:

            info = wikipedia.summary(person, sentences=2)

            speak(info)

        except:

            speak("Wikipedia information not found")

        return True

    # =====================================
    # SYSTEM INFO
    # =====================================

    elif "system status" in text:

        system_info(speak)

        return True

    return False


# =========================================
# MULTI COMMAND EXECUTION
# =========================================


def execute_command(text, speak):

    commands = text.split(" and ")

    handled = False

    for cmd in commands:

        result = execute_single_command(
            cmd.strip(),
            speak
        )

        if result:
            handled = True

    return handled