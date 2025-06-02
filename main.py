import speech_recognition as sr
import pyttsx3
import time
import subprocess
import webbrowser
import os
import platform
import datetime
import random

# Initialize TTS engine with better settings
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Slower, clearer speech
engine.setProperty('volume', 0.9)  # Louder volume

# Get system information
SYSTEM = platform.system().lower()

def speak(text):
    """Enhanced text-to-speech with better pronunciation"""
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def setup_microphone_calibration(recognizer, source):
    """One-time microphone setup for better recognition"""
    print("🔧 Setting up microphone... Please be quiet for 2 seconds.")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"✅ Microphone calibrated. Energy threshold: {recognizer.energy_threshold}")

def open_application(app_name):
    """Open applications based on the operating system"""
    app_name = app_name.lower()
    
    try:
        if SYSTEM == "windows":
            # Windows applications
            apps = {
                'youtube': lambda: webbrowser.open('https://www.youtube.com'),
                'whatsapp': lambda: subprocess.Popen(['start', 'whatsapp:'], shell=True),
                'calculator': lambda: subprocess.Popen(['calc.exe']),
                'gmail': lambda: webbrowser.open('https://mail.google.com'),
                'chrome': lambda: subprocess.Popen(['chrome.exe']),
                'notepad': lambda: subprocess.Popen(['notepad.exe']),
                'file explorer': lambda: subprocess.Popen(['explorer.exe']),
                'control panel': lambda: subprocess.Popen(['control.exe']),
                'paint': lambda: subprocess.Popen(['mspaint.exe']),
                'word': lambda: subprocess.Popen(['winword.exe']),
                'excel': lambda: subprocess.Popen(['excel.exe']),
                'powerpoint': lambda: subprocess.Popen(['powerpnt.exe']),
                'spotify': lambda: subprocess.Popen(['spotify.exe']),
                'discord': lambda: subprocess.Popen(['discord.exe']),
                'steam': lambda: subprocess.Popen(['steam.exe']),
                'vlc': lambda: subprocess.Popen(['vlc.exe']),
                'firefox': lambda: webbrowser.get('firefox').open(''),
                'edge': lambda: subprocess.Popen(['msedge.exe']),
            }
        
        elif SYSTEM == "darwin":  # macOS
            apps = {
                'youtube': lambda: webbrowser.open('https://www.youtube.com'),
                'whatsapp': lambda: subprocess.Popen(['open', '-a', 'WhatsApp']),
                'calculator': lambda: subprocess.Popen(['open', '-a', 'Calculator']),
                'gmail': lambda: webbrowser.open('https://mail.google.com'),
                'safari': lambda: subprocess.Popen(['open', '-a', 'Safari']),
                'chrome': lambda: subprocess.Popen(['open', '-a', 'Google Chrome']),
                'finder': lambda: subprocess.Popen(['open', '-a', 'Finder']),
                'textedit': lambda: subprocess.Popen(['open', '-a', 'TextEdit']),
                'spotify': lambda: subprocess.Popen(['open', '-a', 'Spotify']),
                'discord': lambda: subprocess.Popen(['open', '-a', 'Discord']),
                'vlc': lambda: subprocess.Popen(['open', '-a', 'VLC']),
            }
        
        else:  # Linux
            apps = {
                'youtube': lambda: webbrowser.open('https://www.youtube.com'),
                'whatsapp': lambda: subprocess.Popen(['whatsapp-desktop']),
                'calculator': lambda: subprocess.Popen(['gnome-calculator']),
                'gmail': lambda: webbrowser.open('https://mail.google.com'),
                'firefox': lambda: subprocess.Popen(['firefox']),
                'chrome': lambda: subprocess.Popen(['google-chrome']),
                'file manager': lambda: subprocess.Popen(['nautilus']),
                'terminal': lambda: subprocess.Popen(['gnome-terminal']),
                'text editor': lambda: subprocess.Popen(['gedit']),
                'spotify': lambda: subprocess.Popen(['spotify']),
                'discord': lambda: subprocess.Popen(['discord']),
                'vlc': lambda: subprocess.Popen(['vlc']),
            }
        
        # Try to find and open the application
        for key, func in apps.items():
            if key in app_name or app_name in key:
                func()
                return True
        
        return False
        
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        return False

def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    """Get current date"""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y")

def process_command(text):
    """Process voice commands and respond accordingly"""
    text = text.lower().strip()
    
    # Greeting responses
    if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Good to hear from you! How may I help?",
            "Hello! Ready to help with whatever you need."
        ]
        speak(random.choice(greetings))
        return True
    
    # How are you responses
    elif any(phrase in text for phrase in ['how are you', 'how do you do', 'how are things']):
        responses = [
            "I'm doing great, thank you for asking! How are you?",
            "I'm functioning perfectly and ready to help!",
            "All systems running smoothly! How can I assist you today?",
            "I'm excellent, thanks! What would you like me to do?"
        ]
        speak(random.choice(responses))
        return True
    
    # Thank you responses
    elif any(word in text for word in ['thank you', 'thanks', 'appreciate']):
        responses = [
            "You're very welcome!",
            "Happy to help!",
            "My pleasure!",
            "Anytime! That's what I'm here for."
        ]
        speak(random.choice(responses))
        return True
    
    # Open applications
    elif 'open' in text:
        # Extract app name after 'open'
        parts = text.split('open', 1)
        if len(parts) > 1:
            app_name = parts[1].strip()
            
            # Handle special cases
            if 'youtube' in app_name:
                webbrowser.open('https://www.youtube.com')
                speak("Opening YouTube for you.")
                return True
            elif 'gmail' in app_name or 'email' in app_name:
                webbrowser.open('https://mail.google.com')
                speak("Opening Gmail for you.")
                return True
            elif 'whatsapp' in app_name:
                if open_application('whatsapp'):
                    speak("Opening WhatsApp.")
                else:
                    webbrowser.open('https://web.whatsapp.com')
                    speak("Opening WhatsApp Web.")
                return True
            elif 'calculator' in app_name:
                if open_application('calculator'):
                    speak("Opening calculator.")
                else:
                    speak("Sorry, I couldn't open the calculator.")
                return True
            else:
                # Try to open any other application
                if open_application(app_name):
                    speak(f"Opening {app_name}.")
                else:
                    speak(f"Sorry, I couldn't find or open {app_name}. Let me try opening it in the browser.")
                    try:
                        webbrowser.open(f"https://www.google.com/search?q={app_name}")
                    except:
                        pass
                return True
    
    # Time and date queries
    elif any(word in text for word in ['time', 'clock']):
        current_time = get_time()
        speak(f"The current time is {current_time}")
        return True
    
    elif any(word in text for word in ['date', 'today', 'day']):
        current_date = get_date()
        speak(f"Today is {current_date}")
        return True
    
    # Search queries
    elif any(word in text for word in ['search', 'google', 'find']):
        query = text.replace('search', '').replace('google', '').replace('find', '').strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query} on Google.")
        else:
            speak("What would you like me to search for?")
        return True
    
    # Weather (opens weather website)
    elif 'weather' in text:
        webbrowser.open('https://www.weather.com')
        speak("Opening weather information for you.")
        return True
    
    # News
    elif 'news' in text:
        webbrowser.open('https://news.google.com')
        speak("Opening Google News for you.")
        return True
    
    # Music
    elif any(word in text for word in ['music', 'song', 'play']):
        if 'spotify' in text:
            open_application('spotify')
            speak("Opening Spotify.")
        else:
            webbrowser.open('https://music.youtube.com')
            speak("Opening YouTube Music for you.")
        return True
    
    # Social media
    elif 'facebook' in text:
        webbrowser.open('https://www.facebook.com')
        speak("Opening Facebook.")
        return True
    elif 'instagram' in text:
        webbrowser.open('https://www.instagram.com')
        speak("Opening Instagram.")
        return True
    elif 'twitter' in text:
        webbrowser.open('https://www.twitter.com')
        speak("Opening Twitter.")
        return True
    
    # Help command
    elif 'help' in text or 'what can you do' in text:
        help_text = """I can help you with many things! Here are some examples:
        - Open applications like YouTube, WhatsApp, Calculator, Gmail
        - Tell you the current time and date
        - Search Google for information
        - Open websites like Facebook, Instagram, Twitter
        - Play music on Spotify or YouTube Music
        - Check weather and news
        - Have friendly conversations with you
        Just speak naturally and I'll do my best to help!"""
        speak(help_text)
        return True
    
    # Exit commands
    elif any(word in text for word in ['goodbye', 'bye', 'stop assistant', 'quit', 'exit']):
        farewell = [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Bye! It was nice talking with you!",
            "Until next time! Have a wonderful day!"
        ]
        speak(random.choice(farewell))
        return False  # This will stop the assistant
    
    # Default conversational response
    else:
        responses = [
            "That's interesting! Is there anything specific I can help you with?",
            "I understand. How can I assist you today?",
            "Thanks for sharing that with me. What would you like me to do?",
            "I hear you! Is there a task I can help you with?",
            "That's nice to know. What can I do for you right now?"
        ]
        speak(random.choice(responses))
        return True

def listen_and_recognize(recognizer, source, retries=5):
    """Enhanced speech recognition with multiple engines and better settings"""
    
    # Optimized recognizer settings for better accuracy
    recognizer.energy_threshold = max(recognizer.energy_threshold, 300)
    recognizer.dynamic_energy_adjustment_ratio = 1.15
    recognizer.pause_threshold = 0.8  # Wait longer for complete sentences
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5
    
    for attempt in range(retries):
        try:
            print(f"🎙 Listening... (attempt {attempt + 1}/{retries})")
            if attempt == 0:
                speak("I'm ready to listen. How can I help you?")
            
            # Listen with longer timeout for complete thoughts
            audio = recognizer.listen(
                source, 
                timeout=8,  # Wait longer for user to start speaking
                phrase_time_limit=15  # Allow longer phrases
            )
            
            print("⏳ Processing your speech...")
            
            # Primary recognition with Google (most accurate)
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                if text.strip():  # Make sure we got actual text
                    return text.strip()
            except:
                pass
            
            # Backup recognition with Google (different language model)
            try:
                text = recognizer.recognize_google(audio, language='en-IN')
                if text.strip():
                    return text.strip()
            except:
                pass
            
            # If Google fails, try offline recognition
            try:
                text = recognizer.recognize_sphinx(audio)
                if text.strip():
                    print("📱 Used offline recognition")
                    return text.strip()
            except:
                pass
                
        except sr.UnknownValueError:
            if attempt < retries - 1:
                print("❌ Couldn't understand. Let me try again...")
                speak("I didn't catch that. Please speak a bit louder and clearer.")
                time.sleep(0.5)
            else:
                print("❌ Still couldn't understand after multiple attempts.")
                speak("I'm having trouble understanding. Let's try again from the beginning.")
                
        except sr.RequestError as e:
            print(f"⚠ Network issue: {e}")
            speak("I'm having internet connection problems. Let me try offline recognition.")
            # Try offline recognition as backup
            try:
                text = recognizer.recognize_sphinx(audio)
                if text.strip():
                    print("📱 Used offline backup")
                    return text.strip()
            except:
                if attempt < retries - 1:
                    speak("Let me try again with a different approach.")
                    time.sleep(1)
                
        except sr.WaitTimeoutError:
            if attempt < retries - 1:
                print("⌛ Timeout. Trying again...")
                speak("I didn't hear anything. Please try speaking again.")
                time.sleep(0.5)
            else:
                print("⌛ Multiple timeouts.")
                speak("I'm not hearing any speech. Please check your microphone.")
                
        except Exception as e:
            print(f"🚨 Unexpected error: {e}")
            if attempt < retries - 1:
                speak("Something went wrong. Let me try again.")
                time.sleep(0.5)
    
    return None  # Failed after all retries

def main():
    recognizer = sr.Recognizer()
    microphone_calibrated = False
    
    print("🤖 Smart Voice Assistant Starting...")
    print("💡 I can open apps, answer questions, and have conversations!")
    print("📝 Try saying: 'Open YouTube', 'What time is it?', 'Hello', etc.")
    print("🛑 Say 'goodbye' or press Ctrl+C to stop")
    
    try:
        with sr.Microphone() as source:
            # One-time calibration
            if not microphone_calibrated:
                setup_microphone_calibration(recognizer, source)
                microphone_calibrated = True
                speak("Voice assistant is ready! I can help you open applications, answer questions, and chat with you. How can I help you today?")
            
            print("\n🔁 Voice Assistant is active and listening...")
            
            while True:
                result = listen_and_recognize(recognizer, source)
                
                if result:
                    print(f"\n✅ You said: '{result}'")
                    print("-" * 50)
                    
                    # Process the command
                    continue_running = process_command(result)
                    
                    if not continue_running:
                        break
                    
                else:
                    print("❌ Could not understand speech after multiple attempts.")
                    speak("I couldn't understand what you said. Please try again or say 'help' to see what I can do.")
                
                print("\n" + "="*60)
                time.sleep(0.5)  # Brief pause before next listening cycle
                
    except KeyboardInterrupt:
        print("\n\n🛑 Voice assistant stopped by Harsh.")
        speak("Voice assistant stopped. Goodbye!")
    except Exception as e:
        print(f"\n🚨 Fatal Error: {e}")
        speak("A critical error occurred. Shutting down.")


if __name__ == "__main__":
    main()