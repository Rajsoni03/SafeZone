
import speech_recognition as sr

filename='speech.wav'

r=sr.Recognizer()

with sr.AudioFile(filename) as source:
    print('Say Something!')
    audio_data = r.record(source)
    print('Done!')
   
   
   
try:  
    text=r.recognize_google(audio_data)
    print(text)

except Exception as e:
    print (e)