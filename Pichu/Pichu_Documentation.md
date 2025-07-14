# Pichu AI Assistant - Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Feature List](#feature-list)
3. [System Architecture](#system-architecture)
4. [Folder & File Structure](#folder--file-structure)
5. [Intent Recognition (AI/ML)](#intent-recognition-aiml)
6. [Fallback to Gemini API](#fallback-to-gemini-api)
7. [Automation Features](#automation-features)
8. [Image Analysis](#image-analysis)
9. [Voice Features](#voice-features)
10. [Frontend (Web UI)](#frontend-web-ui)
11. [How to Add More Intents](#how-to-add-more-intents)
12. [How to Run/Deploy](#how-to-rundeploy)
13. [Known Issues & Limitations](#known-issues--limitations)
14. [Future Work & Improvements](#future-work--improvements)
15. [Screenshots & Flowchart](#screenshots--flowchart)
16. [Libraries & APIs Used](#libraries--apis-used)

---

## Project Overview

**Pichu** is a modular, AI-powered personal assistant that can:
- Understand user queries using intent recognition (SVM/TF-IDF)
- Automate OS tasks (open apps, control system settings)
- Answer general questions using Google Gemini API
- Perform web searches, fetch weather, tell jokes/facts
- Analyze images (OCR and face detection)
- Interact via a modern web UI with voice input/output

This project demonstrates full-stack development, AI/ML integration, and practical automation.

---

## Feature List

- **Intent Recognition:** Classifies user queries using SVM and TF-IDF.
- **Gemini API Fallback:** Handles open-ended or unknown queries with Google Gemini.
- **OS Automation:** Open Notepad, Calculator, File Explorer, Command Prompt, etc.
- **System Control:** Adjust volume, brightness, WiFi, shutdown, restart, sleep.
- **Web Search:** Google, YouTube, Wikipedia, ChatGPT.
- **Weather Info:** Fetches real-time weather for any city.
- **Jokes & Facts:** Responds with random jokes and facts.
- **Image Analysis:** Extracts text and detects faces from uploaded images.
- **Voice Input/Output:** Uses browser and backend TTS for speech.
- **Conversation History:** Remembers previous exchanges for context.
- **Modern Web UI:** Responsive chat interface with voice and file upload.

---

## System Architecture

```
[User (Web/CLI)]
      |
      v
[Frontend (index.html, JS)]
      |
      v
[Flask Backend (app.py)]
      |
      +--> [main.py] --+--> [Model.py (PichuModel)] --+--> [Intent Recognition (SVM/TF-IDF)]
      |                |                              |
      |                |                              +--> [Gemini API Fallback]
      |                +--> [Automation.py (PichuAI)] +--> [OS Automation, Weather, Web Search]
      |                +--> [os_utils.py]             +--> [Conversation History]
      |                +--> [image.py]                +--> [Image Analysis]
      |
      v
[Response to User (Text + Speech)]
```

---

## Folder & File Structure

```
Pichu/
│
├── Backend/
│   ├── app.py                # Flask app entry point
│   ├── main.py               # Main backend logic and query handler
│   ├── Automation.py         # Automation features (PichuAI)
│   ├── Model.py              # Intent recognition (PichuModel)
│   ├── os_utils.py           # OS-level utilities
│   ├── image.py              # Image OCR and face detection
│   ├── static/               # Frontend assets (JS, CSS, images, audio)
│   ├── templates/            # HTML templates (index.html)
│   └── __pycache__/          # Python bytecode cache
├── config.json               # Project configuration
├── debug.log                 # Log file
└── __pycache__/              # Python bytecode cache
```

---

## Intent Recognition (AI/ML)

- **Model:** SVM (Support Vector Machine) with TF-IDF vectorization.
- **Purpose:** Classifies user queries into predefined intents (greeting, weather, jokes, etc.).
- **How it works:**  
  - User input is vectorized using TF-IDF.
  - SVM predicts the intent.
  - If intent is recognized, a random response from that intent is returned.

---

## Fallback to Gemini API

- **When used:** If the user's query does not match any known intent.
- **How it works:**  
  - The query (and optionally recent conversation context) is sent to Gemini.
  - Gemini generates a concise, relevant response.
- **Prompting:** The prompt is prefixed with instructions to keep responses short and clear.

---

## Automation Features

- **OS Automation:** Open apps (Notepad, Calculator, etc.), control system settings (volume, brightness, WiFi), shutdown/restart/sleep.
- **Web Automation:** Open Google, YouTube, Wikipedia, ChatGPT, Brave browser.
- **Weather:** Fetches weather using OpenWeatherMap API.
- **Music:** Play, list, and control music playback.

---

## Image Analysis

- **OCR:** Uses pytesseract to extract text from images.
- **Face Detection:** Uses OpenCV to detect faces in uploaded images.
- **Web Integration:** Users can upload images via the web UI; backend processes and returns results.

---

## Voice Features

- **Voice Input:** Uses Web Speech API for speech-to-text in the browser.
- **Voice Output:** Uses Web Speech API for TTS in the browser; uses pyttsx3 for TTS in CLI mode.
- **Voice Selection:** Users can choose their preferred voice in the web UI.

---

## Frontend (Web UI)

- **index.html:** Responsive chat interface with voice and file upload.
- **script.js:** Handles chat logic, voice input/output, and file uploads.
- **style.css:** Custom styles for the UI.
- **pichu.png:** Assistant logo.

---

## How to Add More Intents

1. Open `Model.py`.
2. Add a new intent to the `intents` dictionary:
   ```python
   "new_intent": {
       "patterns": ["pattern1", "pattern2"],
       "responses": ["response1", "response2"]
   }
   ```
3. Retrain the model if needed.

---

## How to Run/Deploy

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set up API keys in `config.json` if needed.
3. Run the backend:
   ```
   python Backend/app.py
   ```
4. Open the web UI at `http://localhost:5000`.

---

## Known Issues & Limitations

- Web Speech API voices are limited by the user's OS/browser.
- Gemini API requires an API key and internet connection.
- Some OS automation features may not work on all platforms.
- No user authentication or personalization yet.

---

## Future Work & Improvements

- Add user authentication and personalization.
- Integrate reminders and calendar features.
- Use a cloud TTS API for more natural speech.
- Add a mobile app or PWA support.
- Improve context memory with embeddings or vector database.
- Add more automation and smart home integration.

---

## Screenshots & Flowchart

*(Add screenshots of your UI and a diagram based on the architecture above)*

---

## Libraries & APIs Used

- **Python:** Flask, scikit-learn, pyttsx3, speech_recognition, wikipedia, requests, pytesseract, opencv-python, screen_brightness_control, pycaw
- **Frontend:** Web Speech API, Tailwind CSS, Chart.js, Lucide Icons
- **APIs:** Google Gemini, OpenWeatherMap

---

# End of Documentation
