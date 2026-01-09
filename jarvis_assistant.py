import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyttsx3 # Keep this import
import speech_recognition as sr # Keep this import

# --- 2.1: Initialize the Engine ---
# pyttsx3 uses SAPI5 (Windows), NSSpeechSynthesizer (Mac), or eSpeak (Linux)
engine = pyttsx3.init()

# Optional: Customize the voice rate (speed)
# rate = engine.getProperty('rate')
# engine.setProperty('rate', 150) # Lower number = slower speech

# --- 2.2: Define the Speak Function ---
def speak(text):
    """Converts the given text string to speech."""
    engine.say(text)
    engine.runAndWait() # This blocks until the speech is finished
    print(f"Assistant: {text}")

# Test the function
speak("Hello, sir. Initializing system checks.")

def takeCommand():
    """Captures microphone input, converts it to text, and handles errors."""
    r = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("\nListening...")
        
        # Adjust for ambient noise to improve recognition accuracy
        r.pause_threshold = 1 # Seconds of non-speaking data before a phrase is considered complete
        r.adjust_for_ambient_noise(source, duration=1) 
        
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        # Use Google's API for reliable, free, cloud-based recognition
        query = r.recognize_google(audio, language='en-US') 
        print(f"User said: {query}")

    except sr.UnknownValueError:
        # User spoke, but the service couldn't understand the words
        print("Recognition failed. Please say that again.")
        return "None"
    
    except sr.RequestError as e:
        # Failed to connect to the Google service (e.g., no internet or rate limit)
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
        
    return query.lower() # Return the recognized command in lowercase

# (Keep all previous imports and function definitions: speak() and takeCommand())

def run_jarvis_logic(command):
    """Executes an action based on the recognized command."""
    
    # --- Time Command ---
    if 'time' in command:
        # Get current time in 12-hour format
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {current_time}")

    # --- Web Browser Command ---
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube now.")

    # --- Application Launch Command (Windows Example) ---
    elif 'open code' in command:
        # **IMPORTANT**: Replace this path with the path to the executable file
        # of the program you want to open (e.g., VS Code, Chrome, etc.)
        # On Mac, it's typically 'open -a "Application Name"'
        try:
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe" # Windows path example
            os.startfile(codePath)
            speak("Launching Visual Studio Code.")
        except FileNotFoundError:
            speak("Sorry, I could not find that application path.")

    # --- Exit Command ---
    elif 'exit' in command or 'stop listening' in command:
        speak("Understood. System shutting down. Goodbye.")
        return False # Signal to end the loop
    
    # --- Default/Fallback Response ---
    else:
        # This prevents the assistant from using a costly AI API
        speak("I am sorry, I am currently programmed only for basic time and application commands.")

    return True # Signal to continue listening
# (Keep all previous code)

if __name__ == "__main__":
    
    # Initialize the greeting
    # You can add the "wishMe" function mentioned in the search results here!
    speak("System initialization complete. How can I assist you today?")
    
    should_continue = True
    
    while should_continue:
        command = takeCommand()
        
        # Only process the command if something was actually recognized
        if command != "none":
            should_continue = run_jarvis_logic(command)