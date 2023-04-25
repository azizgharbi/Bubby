import asyncio
import sys
import speech_recognition as sr
from Bot import Bot


async def main():
    bot = Bot()
    reply = "Nothing, Can you repeat"

    try:
        prompt = sys.argv[1]
        reply = bot.make_request(prompt)
    except:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please say something...")
            # Record the audio
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                reply = bot.make_request(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Error with the Google Speech Recognition service: {e}")

    print(reply)


asyncio.run(main())
