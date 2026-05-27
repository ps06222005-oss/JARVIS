import speech_recognition as sr
import pyttsx3
import ollama
import webbrowser
import pyautogui
import cv2
from voice import speak
from datetime import datetime
from commands import execute_command
from brain import ask_ai
from voice import speak
from listen import listen



speak("Jarvis is online")


while True:

    command = listen()

    if not command:
        continue

    if "exit" in command or "stop" in command:

        speak("Goodbye sir")

        break

    handled = execute_command(
        command,
        speak
    )

    if not handled:

        response = ask_ai(command)

        speak(response)

# =========================
# VOICE ENGINE
# =========================

engine = pyttsx3.init()

engine.setProperty("rate", 180)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# =========================
# SPEAK
# ========================
import asyncio
import edge_tts
import pygame
import uuid
import os

pygame.mixer.init()


async def speak_async(text):

    if not text:
        return

    print(f"\nJarvis: {text}\n")

    # UNIQUE FILE NAME
    file_name = f"{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text,
        "en-IN-PrabhatNeural"
    )

    await communicate.save(file_name)

    pygame.mixer.music.load(file_name)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    os.remove(file_name)


def speak(text):
    asyncio.run(speak_async(text))

# =========================
# SPEECH RECOGNITION
# =========================

recognizer = sr.Recognizer()

def listen():

    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        print("Recognizing...")

        text = recognizer.recognize_google(audio)

        print(f"You: {text}")

        return text.lower()

    except sr.WaitTimeoutError:

        print("No speech detected")
        return ""

    except sr.UnknownValueError:

        print("Could not understand")
        return ""

    except Exception as e:

        print("Error:", e)
        return ""

# =========================
# MEMORY
# =========================

chat_memory = [
    {
        "role": "system",
        "content": (
            "You are Jarvis, a smart AI assistant. "
            "Reply shortly and naturally."
        )
    }
]

# =========================
# AI BRAIN
# =========================

def ask_ai():

    response = ollama.chat(
        model="llama3:8b",
        messages=chat_memory
    )

    return response["message"]["content"]

# =========================
# VISION
# =========================

def vision_ai():

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

    speak("Analyzing image")

    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": "Describe what you see",
                "images": [image_path]
            }
        ]
    )

    result = response["message"]["content"]

    speak(result)

# =========================
# MAIN
# =========================

speak("Jarvis is online.")

while True:

    text = listen()

    if text == "":
        continue

    # =====================
    # EXIT
    # =====================

    if "shutdown" in text or "bye" in text or "exit" in text:

        speak("Goodbye")
        break

    # =====================
    # TIME
    # =====================

    elif "time" in text:

        current_time = datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

    # =====================
    # OPEN YOUTUBE
    # =====================

    elif "open youtube" in text:

        speak("Opening YouTube for you")

        webbrowser.open("https://youtube.com")

    # =====================
    # OPEN GOOGLE
    # =====================

    elif "open google" in text:

        speak("Opening Google")

        webbrowser.open("https://google.com")

    # =====================
    # PLAY SONG
    # =====================

    elif "play" in text:

        song = text.replace("play", "").strip()

        if song == "":

            speak("Tell me the song name")

        else:

            speak(f"Playing {song}")

            url = (
                "https://www.youtube.com/results?"
                f"search_query={song}"
            )

            webbrowser.open(url)

    # =====================
    # CAMERA VISION
    # =====================

    elif (
        "vision" in text
        or "camera" in text
        or "what do you see" in text
    ):

        vision_ai()

    # =====================
    # AI CHAT
    # =====================

    else:

        chat_memory.append(
            {
                "role": "user",
                "content": text
            }
        )

        answer = ask_ai()

        chat_memory.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        speak(answer)