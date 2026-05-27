import speech_recognition as sr


def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.adjust_for_ambient_noise(
            source,
            duration=1
        )

        try:

            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:

            print("No speech detected")

            return ""

    try:

        print("Recognizing...")

        text = r.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Could not understand")

        return ""

    except Exception as e:

        print("Recognition Error:", e)

        return ""