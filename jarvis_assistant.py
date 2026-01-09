import os
import datetime
import webbrowser
import wikipedia # Core library for Wikipedia lookup

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

def search_wikipedia(query):
    """Searches Wikipedia and speaks the first two sentences of the summary."""
    try:
        # Set the number of sentences to return (we use 2 for a quick answer)
        speak(f"Searching Wikipedia for {query}")
        
        # This performs the search
        results = wikipedia.summary(query, sentences=2, auto_suggest=False, redirect=True)
        
        # The AI needs to confirm what it found
        speak("According to Wikipedia...")
        speak(results)

    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I could not find any Wikipedia page for {query}.")
    
    except wikipedia.exceptions.DisambiguationError as e:
        # This occurs if the query is ambiguous (e.g., 'Jordan')
        speak(f"Your search for {query} is ambiguous. Please be more specific.")
        print(f"Disambiguation options: {e.options}")
    
    except Exception as e:
        speak("An error occurred while accessing Wikipedia.")
        print(f"Wikipedia Error: {e}")


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
        # Uses Google's API for speech-to-text
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
    
    # --- Time Command (PREVIOUS FEATURE) ---
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {current_time}")

    # --- Web Browser Command (PREVIOUS FEATURE) ---
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube now.")

    # --- Wikipedia Command (NEW FEATURE) ---
    elif 'wikipedia' in command or 'search' in command:
        speak('What should I search for?')
        topic = takeCommand()
        
        if topic != 'none':
            # Clean the topic by removing the trigger word
            cleaned_topic = topic.replace('wikipedia', '').replace('search', '').strip()
            
            if cleaned_topic:
                search_wikipedia(cleaned_topic)
            else:
                speak("I need a topic to search, sir.")
        else:
            speak("I didn't catch the topic. Try again.")


    # --- Application Launch Command (PREVIOUS FEATURE) ---
    elif 'open code' in command:
        try:
            # IMPORTANT: For Mac, a common command is: os.system('open -a "Visual Studio Code"')
            # You currently have a Windows path. Please update this line for your macOS machine:
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe" 
            os.startfile(codePath) 
            speak("Launching Visual Studio Code.")
        except FileNotFoundError:
            speak("Sorry, I could not find that application path. Please update the path for your operating system.")

    # --- Exit Command (PREVIOUS FEATURE) ---
    elif 'exit' in command or 'stop listening' in command:
        speak("Understood. System shutting down. Goodbye.")
        return False 
    
    # --- Default/Fallback Response ---
    else:
        speak("I am sorry, I am currently programmed only for basic time, search, and application commands.")

    return True 

if __name__ == "__main__":
    
    # Critical check: ensure the wikipedia library is installed
    try:
        import wikipedia
    except ImportError:
        speak("CRITICAL ERROR: Wikipedia library is not installed. Please run 'pip install wikipedia'")
        exit() 

    speak("System initialization complete. How can I assist you today?")
    
    should_continue = True
    
    while should_continue:
        command = takeCommand()
        
        if command != "none":
            should_continue = run_jarvis_logic(command)