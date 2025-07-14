import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import random
import warnings
warnings.simplefilter('ignore')

from .Automation import PichuAI

class PichuModel:
    def __init__(self, api_key: str):
        # --- Chatbot/Intent Model ---
        self.new_method()
        self.training_data = []
        self.labels = []
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                self.training_data.append(pattern.lower())
                self.labels.append(intent)
        self.vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(), stop_words="english", max_df=0.8, min_df=1)
        X = self.vectorizer.fit_transform(self.training_data)
        X_train, X_test, Y_train, Y_test = train_test_split(X, self.labels, test_size=0.4, random_state=42, stratify=self.labels)
        self.model = SVC(kernel='linear', probability=True, C=1.0)
        self.model.fit(X_train, Y_train)

        # --- AI Module ---
        self.ai = PichuAI(api_key)

    def new_method(self):
        self.intents = {
            "greetings": {
                "patterns": ["hello pichu", "hi pichu", "hey pichu", "what's up pichu", "how are you pichu", "hi there pichu"],
                "responses": ["Pi Pichu! How can I assist you?", "Pi-Pi Pichu!⚡️", "Pi Pichuuu! What can I do for you?"]
            },
            "goodbye": {
                "patterns": ["bye pichu", "see you later pichu", "goodbye pichu", "farewell pichu", "catch you later pichu"],
                "responses": ["Goodbye!", "See you later!", "Have a great day!"]
            },
            "gratitude": {
                "patterns": ["thank you pichu", "thanks pichu", "appreciate it pichu", "thank you so much pichu", "thanks a lot pichu", "much appreciated pichu"],
                "responses": ["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!"]
            },
            "apologies": {
                "patterns": ["sorry", "my apologies", "apologize", "I'm sorry"],
                "responses": ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay."]
            },
            "positive_feedback": {
                "patterns": ["great job", "well done", "awesome", "fantastic", "amazing work", "excellent"],
                "responses": ["Thank you! I appreciate your feedback.", "Glad to hear that!", "Thank you for the compliment!"]
            },
            "negative_feedback": {
                "patterns": ["not good", "disappointed", "unsatisfied", "poor service", "needs improvement", "could be better"],
                "responses": ["I'm sorry to hear that. Can you please provide more details so I can assist you better?", "I apologize for the inconvenience. Let me help resolve the issue."]
            },
            "help": {
                "patterns": ["help", "can you help me?", "I need assistance", "support"],
                "responses": ["Sure, I'll do my best to assist you.", "Of course, I'm here to help!", "How can I assist you?"]
            },
            "name": {
                "patterns": ["what's your name","what is your name", "tell me about yourself", "what are you", "identify yourself", "who are you"],
                "responses": [
                    "My name is Pichu !",
                    "I am Pichu, your personal AI assistant created by my Master.",
                    "I am an AI model created by my Master and My Name is Pichu !.",
                    "My name is Pichu and I am an AI model created by my Master, I have access to Google API which helps me generate real-time queries."
                ]
            },
            "jokes": {
                "patterns": ["tell me a joke", "joke please", "got any jokes?", "make me laugh"],
                "responses": [
                    "Why did the chicken cross the road? To get to the other side!",
                    "I'm reading a book on anti-gravity. It's impossible to put down!",
                    "Why did the computer show up at work late? It had a hard drive!",
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "Why did the chicken join a band? Because it had the drumsticks!"
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the scarecrow win an award? Because he was outstanding in his field!"
                ]
            },
            "facts": {
                "patterns": ["tell me a fact", "fact please", "got any fun fact?", "you know any facts"],
                "responses": [
                    "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs!",
                    "Bananas are berries, but strawberries aren't.",
                    "Octopuses have three hearts."
                    "Did you know? Honey never spoils.",
                    "A group of flamingos is called a 'flamboyance'.",
                    "Bananas are berries, but strawberries aren't."
                ]
            },
        }

    def speak(self, text):
        print(f"==> Pichu : {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def speechrecognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.....")
            r.pause_threshold = 1
            audio = r.listen(source, 0, 8)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language="en-hi")
            print(f"==> User : {query}")
            return query.lower()
        except:
            return ""

    def predict_intent(self, user_input):
        user_input = user_input.lower()
        input_vector = self.vectorizer.transform([user_input])
        intent = self.model.predict(input_vector)[0]
        return intent

    def get_response(self, intent):
        if intent in self.intents:
            return random.choice(self.intents[intent]['responses'])
        return None

    def handle_chat(self, user_input):
        intent = self.predict_intent(user_input)
        return self.get_response(intent)

    def handle_ai_query(self, query, language="en"):
        # If language is not English, prompt Gemini to answer in the target language
        if language != "en":
            query = f"Please answer in {language}: {query}"
        return self.ai.answer_query(query)

    def get_intent_response(self, query):
        query = query.lower()
        for intent, data in self.intents.items():
            for pattern in data.get("patterns", []):
                if pattern in query:
                    responses = data.get("responses", [])
                    if responses:
                        return random.choice(responses)
        return None  # No match found
