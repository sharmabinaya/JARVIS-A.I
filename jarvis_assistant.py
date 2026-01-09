import os
import datetime
import webbrowser

import pyttsx3
import speech_recognition as sr

# --- 2.1: Initialize the Engine ---
engine = pyttsx3.init()

# --- 2.2: Define the Speak Function ---
def speak(text):
    """Converts the given text string to speech."""
    engine.say(text)
    engine.runAndWait() 
    print(f"Assistant: {text}")

# Test the function (You can comment this out after initial run)
# speak("Hello, sir. Initializing system checks.")

def takeCommand():
    """Captures microphone input, converts it to text, and handles errors."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1) 
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-US') 
        print(f"User said: {query}")

    except sr.UnknownValueError:
        print("Recognition failed. Please say that again.")
        return "None"
    
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
        
    return query.lower()

def run_jarvis_logic(command):
    """Executes an action based on the recognized command."""
    
    # --- Time Command ---
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {current_time}")

    # --- Web Browser Command ---
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube now.")

    # --- Application Launch Command (Windows Example) ---
    elif 'open code' in command:
        try:
            # Check this path is correct for your system!
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe" 
            os.startfile(codePath)
            speak("Launching Visual Studio Code.")
        except FileNotFoundError:
            speak("Sorry, I could not find that application path.")

    # --- Exit Command ---
    elif 'exit' in command or 'stop listening' in command:
        speak("Understood. System shutting down. Goodbye.")
        return False 
    
    # --- Default/Fallback Response ---
    else:
        speak("I am sorry, I am currently programmed only for basic time and application commands.")

    return True 

if __name__ == "__main__":
    
    speak("System initialization complete. How can I assist you today?")
    
    should_continue = True
    
    while should_continue:
        command = takeCommand()
        
        if command != "none":
            should_continue = run_jarvis_logic(command)