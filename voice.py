import asyncio
import edge_tts
import pygame
import os

VOICE = "en-US-GuyNeural"

pygame.mixer.init()


async def speak_async(text):

    if not text:
        return

    print(f"\nJarvis: {text}\n")

    file_name = "voice.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(file_name)

    pygame.mixer.music.load(file_name)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    if os.path.exists(file_name):
        os.remove(file_name)


def speak(text):
    asyncio.run(speak_async(text))