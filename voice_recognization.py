import speech_recognition as sr
import pyttsx3
import time

r = sr.Recognizer()
engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

speaking = True

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening... (Say 'stop listening' to pause or 'exit' to quit)")
                audio = r.listen(source)
                mytext = r.recognize_google(audio)
                return mytext
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except Exception as e:
            print(f"An error occurred: {e}")
    return ""

def output_text(text):
    try:
        with open("output.txt", "a") as f:
            f.write(text + "\n")
        print("Text written to file.")
    except Exception as e:
        print(f"Error writing to file: {e}")

def speak_text(text):
    try:
        if speaking:
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
        else:
            print("Speech output is paused.")
    except Exception as e:
        print(f"Error in speech output: {e}")

def control_flow(text):
    global speaking
    if 'stop listening' in text.lower():
        print("Pausing speech recognition...")
        return False
    elif 'pause speaking' in text.lower():
        speaking = False
        print("Speech synthesis paused.")
    elif 'resume speaking' in text.lower():
        speaking = True
        print("Speech synthesis resumed.")
    elif 'exit' in text.lower():
        print("Exiting program...")
        return True
    return False

while True:
    text = record_text()
    if text:
        print(f"Recognized Text: {text}")
        output_text(text)
        speak_text(text)
        if control_flow(text):
            break
    else:
        print("No speech was recognized.")
    time.sleep(0.5)
