from flask import Flask, render_template, request, jsonify
import webbrowser
import pyttsx3
import requests
import speech_recognition as sr
import google.generativeai as genai

app = Flask(__name__)

# Initialize speech engine and generative AI model
engine = pyttsx3.init()
newsapi = "cb181f3461b04bd8ac3a1f6ab478b56a"

# Configure Google Gemini API
genai.configure(api_key="AIzaSyC20mjRJZxKd6FUMmrWNnpTRJsE_DrorFE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to handle speech synthesis
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Process user commands
def process_command(command):
    response = ""
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
        response = "Opening Google."
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
        response = "Opening Facebook."
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        response = f"Playing {song}"  # You may want to add the actual song playing logic
    elif "news" in command.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                response = f"Here are the top {len(articles)} headlines."
                for article in articles[:5]:
                    response += f"\n{article['title']}"
            else:
                response = "Sorry, I couldn't fetch the news."
        except Exception as e:
            response = "An error occurred while fetching the news."
    else:
        # Send the command to Gemini AI
        try:
            ai_response = model.generate_content(command)
            response = ai_response.text
        except Exception as e:
            response = "There was an issue processing your request."

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def run_command():
    try:
        data = request.get_json()
        command = data.get('command')
        response = process_command(command)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"An error occurred: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
