
import speech_recognition as sr

filename='speech.wav'
#1.Convert the format of audio from (.ogg)to (.wav)
#2.Make sure that the program file and the audio file will there in same folder

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
