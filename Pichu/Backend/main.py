import sys
import os
import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
from Model import PichuModel
from Automation import PichuAI, play_music, play_specific_song, list_songs, search_google, search_wiki, search_youtube, search_chatgpt
import os_utils

# --- TTS Setup ---

if sys.platform == "win32":
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)

def speak(text):
    print(f"Pichu: {text}")
    engine.say(text)
    engine.runAndWait()
    
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"==> Master : {query}")
        return query
    except Exception:
        speak("Sorry, I did not understand that. Could you please repeat?")
        return input("Type your command: ")


# --- Main Query Handler ---
API_KEY = "AIzaSyBvTHlUDojbUvr3V-cuRkFHgyUkrKvgU4E"
pichu_model = PichuModel(api_key=API_KEY)
automation = PichuAI(api_key=API_KEY)

def handle_query(query):
    query = query.lower().strip()
    
   
    # ---------- OS and system commands -----------  
    if "open notepad" in query:
        return os_utils.open_app("notepad")
    
    elif "open calculator" in query:
        return os_utils.open_app("calculator")
    
    elif "open command prompt" in query or "open cmd" in query:
        return os_utils.open_app("cmd")
    
    elif "open file explorer" in query or "open explorer" in query:
        return os_utils.open_app("explorer")
    
    elif "open settings" in query:
        return os_utils.open_app("settings")
    
    elif "open chatgpt" in query or "open chat gpt" in query:
        return os_utils.open_app("chatgpt")
    
    elif "open brave" in query or "open browser" in query:
        return os_utils.open_app("brave")
    
    elif "shutdown" in query:
        os_utils.shutdown()
        return "Shutting down the system."
    
    elif "restart" in query:
        os_utils.restart()
        return "Restarting the system."
    
    elif "sleep" in query:
        os_utils.sleep()
        return "Putting the system to sleep."
    
    elif "increase brightness" in query or "brightness up" in query:
        os_utils.increase_brightness()
        return "Brightness increased."
    
    elif "decrease brightness" in query or "brightness down" in query:
        os_utils.decrease_brightness()
        return "Brightness decreased."
    
    elif "increase volume" in query or "volume up" in query:
        os_utils.increase_volume()
        return "Volume increased."
    
    elif "decrease volume" in query or "volume down" in query:
        os_utils.decrease_volume()
        return "Volume decreased."
    
    elif "mute volume" in query or "mute" in query:
        os_utils.mute_volume()
        return "Volume muted."
    
    elif "unmute volume" in query or "unmute" in query:
        os_utils.unmute_volume()
        return "Volume unmuted."
    
    elif "turn on wifi" in query or "enable wifi" in query:
        os_utils.enable_wifi()
        return "WiFi enabled."
    
    # ---------- Music Commands -----------
    elif 'play music' in query or 'play song' in query:
        return play_music()
    elif 'next song' in query or 'next music' in query:
        return play_music(next_song=True)
    elif 'list of songs' in query or 'list of music' in query:
        return list_songs()
    elif 'play' in query and len(query.split()) > 1:
        return play_specific_song(query)
   
    # --------- Autiomation Queries ----------
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}."
    elif "open google" in query:
        webbrowser.open("https://google.com")
        return "Opening Google."
    elif query.startswith("search for") or query.startswith("google"):
        return search_google(query)
    elif "open youtube" in query or query.startswith("search on youtube") or query.startswith("youtube"):
        return search_youtube(query)
    elif "on chat gpt" in query or "search on chatgpt" in query:
        return search_chatgpt(query)
    elif "wikipedia" in query or "search on wikipedia" in query:
        return search_wiki(query)
    elif "weather" in query:
        city = automation._extract_city(query) or "Bilaspur"
        return automation.get_weather(city)
    
    elif " image" in query or "text from image" in query or "image recognition" in query:
        from image import analyze_image_text_and_faces
        result = analyze_image_text_and_faces()
        return result
    
    # ----------- History for gemini response -----------
    elif "give me past conversation" in query or "give me history" in query or "show me past conversation" in query:
        history = automation.get_history()
        if not history:
            return "No conversation history found."
        formatted = []
        for idx, item in enumerate(history, 1):
            role = item.get("role", "user")
            content = item.get("content", "")
            formatted.append(f"{idx}. {role.capitalize()}: {content}")
        return "\n".join(formatted)
    

    # --- Intent matching from Model.py ---
    response = pichu_model.get_intent_response(query)
    if response:
        automation.conversation_history.append({"role": "user", "content": query})
        automation.conversation_history.append({"role": "assistant", "content": response})
        return response

    # --- Fallback: Gemini API ---
    automation.conversation_history.append({"role": "user", "content": query})
    response = pichu_model.handle_ai_query(query)
    automation.conversation_history.append({"role": "assistant", "content": response})
    return response

# --- CLI Entry Point ---
def main_cli():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Afternoon!")

    else:
        speak("Evening Master!")

    speak("I am Picchu. Please tell me how may I help you")
    while True:
        query = take_command()
        if not query or query == "none":
            continue
        if 'quit' in query or 'exit' in query:
            speak("Goodbye Sir, have a nice day!")
            break
        response = handle_query(query)
        speak(response)

           # Fallback: AI/Chat/Automation
    return pichu_model.handle_ai_query(query)


if __name__ == "__main__":
        main_cli()
