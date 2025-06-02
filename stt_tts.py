import speech_recognition as sr
import pyttsx3
import time

# Initialize TTS engine with better settings
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Slower, clearer speech
engine.setProperty('volume', 0.9)  # Louder volume

def speak(text):
    """Enhanced text-to-speech with better pronunciation"""
    engine.say(text)
    engine.runAndWait()

def setup_microphone_calibration(recognizer, source):
    """One-time microphone setup for better recognition"""
    print("🔧 Setting up microphone... Please be quiet for 2 seconds.")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f" Microphone calibrated. Energy threshold: {recognizer.energy_threshold}")

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
            print(f"🎙️ Listening... (attempt {attempt + 1}/{retries})")
            if attempt == 0:
                speak("I'm ready to listen. Please speak clearly.")
            
            # Listen with longer timeout for complete thoughts
            audio = recognizer.listen(
                source, 
                timeout=8,  # Wait longer for user to start speaking
                phrase_time_limit=15  # Allow longer phrases
            )
            
            print(" Processing your speech...")
            
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
                    print(" Used offline recognition")
                    return text.strip()
            except:
                pass
                
        except sr.UnknownValueError:
            if attempt < retries - 1:
                print(" Couldn't understand. Let me try again...")
                speak("I didn't catch that. Please speak a bit louder and clearer.")
                time.sleep(0.5)
            else:
                print(" Still couldn't understand after multiple attempts.")
                speak("I'm having trouble understanding. Let's try again from the beginning.")
                
        except sr.RequestError as e:
            print(f" Network issue: {e}")
            speak("I'm having internet connection problems. Let me try offline recognition.")
            # Try offline recognition as backup
            try:
                text = recognizer.recognize_sphinx(audio)
                if text.strip():
                    print(" Used offline backup")
                    return text.strip()
            except:
                if attempt < retries - 1:
                    speak("Let me try again with a different approach.")
                    time.sleep(1)
                
        except sr.WaitTimeoutError:
            if attempt < retries - 1:
                print(" Timeout. Trying again...")
                speak("I didn't hear anything. Please try speaking again.")
                time.sleep(0.5)
            else:
                print(" Multiple timeouts.")
                speak("I'm not hearing any speech. Please check your microphone.")
                
        except Exception as e:
            print(f" Unexpected error: {e}")
            if attempt < retries - 1:
                speak("Something went wrong. Let me try again.")
                time.sleep(0.5)
    
    return None  # Failed after all retries

def main():
    recognizer = sr.Recognizer()
    microphone_calibrated = False
    
    print(" Enhanced Voice Assistant Starting...")
    print(" Tip: Speak clearly and at normal pace for best results")
    print(" Press Ctrl+C to stop")
    
    try:
        with sr.Microphone() as source:
            # One-time calibration
            if not microphone_calibrated:
                setup_microphone_calibration(recognizer, source)
                microphone_calibrated = True
                speak("Voice assistant is ready! I will repeat everything you say.")
            
            print("\n Voice Assistant is active and listening...")
            
            while True:
                result = listen_and_recognize(recognizer, source)
                
                if result:
                    print(f"\n You said: '{result}'")
                    print("-" * 50)
                    
                    # Check for exit commands
                    if any(word in result.lower() for word in ['goodbye', 'bye', 'stop assistant', 'quit', 'exit']):
                        speak(f"You said: {result}")
                        speak("Goodbye! Voice assistant is shutting down.")
                        break
                    
                    # Repeat what user said
                    speak(f"You said: {result}")
                    
                else:
                    print(" Could not understand speech after multiple attempts.")
                    speak("I couldn't understand what you said. Please try again.")
                
                print("\n" + "="*60)
                time.sleep(0.5)  # Brief pause before next listening cycle
                
    except KeyboardInterrupt:
        print("\n\n Voice assistant stopped by Harsh.")
        speak("Voice assistant stopped. Goodbye!")
    except Exception as e:
        print(f"\n Fatal Error: {e}")
        speak("A critical error occurred. Shutting down.")

if __name__ == "__main__":
    main()
