import google.generativeai as genai
import webbrowser
import requests
import random
import os

class PichuAI:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=self.api_key)
        self.model_obj = genai.GenerativeModel(self.model)
        self.conversation_history = []

    def answer_query(self, query: str) -> str:
        prompt = "Answer in 2-3 sentences. Be concise and clear: " + query
        try:
            response = self.model_obj.generate_content(prompt)
            response_text = response.text.strip()
        except Exception as e:
            response_text = f"Error: {str(e)}"
        self.conversation_history.append({"role": "assistant", "content": response_text})
        return response_text
    
    def _gemini_fallback(self, query):
        return self.answer_query(query)

    def get_history(self):
        return self.conversation_history
    
    def _extract_city(self, query):
        words = query.lower().split()
        for i, word in enumerate(words):
            if word == "in" and i + 1 < len(words):
                return words[i + 1]
        return None

    def get_weather(self, city=None):
        api_key = "8fecf4fec91371b88cdb881c5bb7f42f"
        if not city or city.lower() == "my location":
            # Try to get city from IP geolocation
            try:
                ip_info = requests.get("https://ipinfo.io/json").json()
                city = ip_info.get("city", "Bilaspur")
            except Exception:
                city = "Bilaspur"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            res = requests.get(url)
            data = res.json()
            if data.get("cod") == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"The weather in {city.title()} is {desc} with a temperature of {temp}°C."
            else:
                return "Sorry, I couldn't fetch the weather for that city."
        except Exception:
            return "Sorry, I couldn't fetch the weather right now."
        
    
 #----- Web-search Helpers -------
def search_google(query):
    if query.startswith("search for ") or query.startswith("google"):
        search_term = query.replace("search for", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Here are the Google search results for {search_term}."
    else:
        webbrowser.open("https://google.com")
        return "Opening Google."

def search_youtube(query):
    if query.startswith("search on youtube") or query.startswith("youtube"):
        search_term = query.replace("search on youtube", "").replace("youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Here are the YouTube search results for {search_term}."
    else:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

def search_wiki(query):
    if query.startswith("search on wikipedia") or query.startswith("wikipedia") or query.startswith("who is ") or query.startswith("what is "):
        search_term = query.replace("search on wikipedia", "").replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        url = f"https://en.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
        webbrowser.open(url)
        return f"Here are the Wikipedia search results for {search_term}."
    else:
        return None

def search_chatgpt(query):
    if query.startswith("search on chatgpt") or query.startswith("on chat gpt"):
        search_term = query.replace("search on chatgpt", "").replace("on chat gpt", "").strip()
        url = f"https://chat.openai.com/?q={search_term.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Here are the ChatGPT search results for {search_term}."
    else:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT."
        

# --- Music Helpers ---
music_dir = 'D:\\Music'
try:
    songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
except Exception:
    songs = []
last_song_idx = 0

def play_music(next_song=False):
    global last_song_idx
    if not songs:
        return "No music files found in your music directory."
    if next_song:
        last_song_idx = (last_song_idx + 1) % len(songs)
    song_to_play = songs[last_song_idx]
    os.startfile(os.path.join(music_dir, song_to_play))
    return f"Playing {song_to_play}."

def list_songs():
    if not songs:
        return "No music files found in your music directory."
    elif len(songs) > 5:
        return "Here are the list of songs:\n" + "\n".join([f"{idx+1}. {song}" for idx, song in enumerate(songs)])
    else:
        return "\n".join([f"{idx+1}. {song}" for idx, song in enumerate(songs)])

def play_specific_song(query):
    global last_song_idx
    if not songs:
        return "No music files found in your music directory."
    song_name = query.replace('play', '').replace('music', '').strip().lower()
    for idx, song in enumerate(songs):
        if song_name in song.lower():
            last_song_idx = idx
            os.startfile(os.path.join(music_dir, song))
            return f"Playing {song}"
    return "Sorry, I couldn't find that song."

