import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai



music = {
    "shealth": "https://www.youtube.com/watch?v=hYFzyK9ExuM",
    "march": "https://www.youtube.com/watch?v=hYFzyK9ExuM",
    "skyfall":"https://www.youtube.com/watch?v=a3Ue-LN5B9U",
    "wolf":"https://www.youtube.com/watch?v=9N2LvG1dArA"
}

# Initialize recognizer, speech engine, and generative AI model
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "cb181f3461b04bd8ac3a1f6ab478b56a"

# Configure Google Gemini API
genai.configure(api_key="AIzaSyC20mjRJZxKd6FUMmrWNnpTRJsE_DrorFE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Process user commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open insta" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        try:
            # Splitting the command to extract the song name
            song = c.lower().split(" ")[1]
            link = music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I couldn't find the song.")
        except IndexError:
            speak("Please specify a song to play.")
        
    elif "news" in c.lower():
        try:
            # Correct API request format
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if not articles:
                    speak("No news articles found.")
                else:
                    speak(f"Here are the top {len(articles)} headlines.")
                    for article in articles[:5]:  # Limit to 5 articles for brevity
                        speak(article['title'])
                        speak("Moving on to the next headline.")
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("An error occurred while fetching the news.")
    
    # If the command is not understood, send it to Gemini AI for response
    else:
        try:
            # Send the command to Gemini AI
            response = model.generate_content(c)
            answer = response.text
            
            # Speak out the AI's response
            if answer:
                print({answer})
                speak(answer)
            else:
                speak("I couldn't generate a response.")
                
        except Exception as e:
            print(f"Error with Gemini API: {e}")
            speak("There was an issue processing your request.")

# Main logic for Jarvis assistant
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        r = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                audio = r.listen(source, timeout=1, phrase_time_limit=1)
            
            word = r.recognize_google(audio)
            print(f"Recognized word: {word}")  # Debugging output
            
            if word.lower() == "jarvis":
                speak("Yes, master.")
                
                # Listening for command
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=3)
                    command = r.recognize_google(audio)
                    print(f"Recognized command: {command}")  # Debugging output
                    processCommand(command)
                    
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            # speak("I didn't understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("There was an issue connecting to the recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred.")
