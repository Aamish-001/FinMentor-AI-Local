import csv
import pyttsx3

# Initialize the text-to-speech audio engine
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)  # Sets speaking pace
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Selects a clear voice profile
except Exception:
    engine = None

def speak(text):
    """Provides automated text-to-speech voice narrations to the user via terminal"""
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass

def save_feedback(data_row):
    """Appends application logs or feedback directly into a local CSV file"""
    try:
        with open('finmentor_feedback.csv', 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(data_row)
        print("[Local Storage]: System log successfully written to finmentor_feedback.csv")
    except Exception as e:
        print(f"[Storage Error]: Failed to save data to local CSV file: {e}")