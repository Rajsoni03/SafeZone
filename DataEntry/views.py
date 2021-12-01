from django.shortcuts import render
from django.conf import settings
import os
import speech_recognition as sr
from django.core.files.storage import default_storage



rec=sr.Recognizer()


# Create your views here.
def dataEntry(request):
	return render(request, "DataEntry/dataEntry.html")


def speech2text(request):
	text = ""
	if (request.method == 'POST'):
		f = request.FILES['file']

		with default_storage.open(f.name, 'wb+') as destination:
		    for chunk in f.chunks():
		        destination.write(chunk)
		File_name = os.path.join(settings.MEDIA_URL, f.name)
		cwd = os.getcwd()
		print(cwd+File_name)
		File_path = cwd+File_name
		with sr.AudioFile(File_path) as source:
		    audio_data = rec.record(source)
		try:  
		    text=rec.recognize_google(audio_data)
		except Exception as e:
		    print (e)

	params = {
		'text' : text
	}
	return render(request, "DataEntry/dataEntry.html", params)