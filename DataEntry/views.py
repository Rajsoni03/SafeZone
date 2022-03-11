from django.shortcuts import render
from django.conf import settings
import os
import speech_recognition as sr
from django.core.files.storage import default_storage
from .models import Crime
from django.utils.dateparse import parse_datetime
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

rec=sr.Recognizer()


# Create your views here.
def dataEntry(request):
	params = {
		'len' : len(Crime.objects.all())
	}
	return render(request, "DataEntry/dataEntry.html", params)


def speech2text(request):
	text = ""
	status = False
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
		    status = True
		except Exception as e:
		    print (e)

	params = {
		'text' : text,
		'status' : status,
		'len' : len(Crime.objects.all())
	}
	return render(request, "DataEntry/dataEntry.html", params)

def text2analysis(request):
	if request.method == "POST":
		crimes = Crime.objects.all()
		# if str(request.POST['textData']) == "delete":
		# 	for i in crimes:
		# 		i.delete()
		count = 0
		if str(request.POST['textData']) == "removeDuplicate":
			for i in crimes:
				first = True
				for j in Crime.objects.filter(eventID = i.eventID):
					if first:
						first = False
					else:
						j.delete()
						count += 1
		else:
			for i in crimes:
				print(i)
		print("count:", count)
	params = {
		'len' : len(Crime.objects.all())
	}
	return render(request, "DataEntry/dataEntry.html", params)

def save2db(request):
	status = False
	if request.method == "POST":
		eventID				= request.POST['eventID']
		callerSource 		= request.POST['callerSource']
		city 				= request.POST['city']
		district 			= request.POST['district']
		address 			= request.POST['address']
		circle 				= request.POST['circle']
		policeStation 		= request.POST['policeStation']
		zipcode 			= request.POST['zipcode']
		latitude 			= request.POST['lat']
		longitude			= request.POST['long']
		eventtype			= request.POST['eventtype']
		eventsubtype		= request.POST['eventsubtype']
		datetime			= request.POST['datetime']

		try:
			Crime(eventID 		= eventID,
				  callerSource 	= callerSource,
				  city 			= city,
				  district 		= district,
				  circle 		= circle,
				  address 		= address,
				  policeStation = policeStation,
				  zipcode 		= zipcode,
				  latitude 		= latitude,
				  longitude 	= longitude,
				  eventtype 	= eventtype,
				  eventsubtype 	= eventsubtype,
				  datetime 		= parse_datetime(datetime+':00')).save()
			status = True
		except Exception as e:
			print(e)
			
	params = {
		'status' : status,
		'len' : len(Crime.objects.all())
	}
	return render(request, "DataEntry/dataEntry.html", params)

def dataupload(request):
	if request.method == "POST":

		# Save file to server
		f = request.FILES['file']
		with default_storage.open(f.name, 'wb+') as destination:
		    for chunk in f.chunks():
		        destination.write(chunk)


		File_name = os.path.join(settings.MEDIA_URL, f.name)
		cwd = os.getcwd()
		print(cwd+File_name)
		File_path = cwd+File_name

		# read file
		df = pd.read_csv(File_path)

		for index, row in df.iterrows():
			print(index)
			if len(Crime.objects.filter(eventID = row["Event"])) is 0:
	
				Latitude = str(row["Latitude"])
				Longitude = str(row["Longitude"])

				location = geolocator.reverse(Latitude+","+Longitude)
				address = location.raw['address']

				city = address.get('city', '')
				zipcode = address.get('postcode', 0)
				suburb = address.get('suburb', '')

				Crime(eventID 		= row["Event"],
					  callerSource 	= row["Caller Source"],
					  city 			= city,
					  district 		= row["District"],
					  circle 		= row["Circle"],
					  address 		= suburb,
					  policeStation = row["Police Station"],
					  zipcode 		= zipcode,
					  latitude 		= row["Latitude"],
					  longitude 	= row["Longitude"],
					  eventtype 	= row["Event Type"],
					  eventsubtype 	= row["Event Sub-Type"],
					  datetime 		= row["Create Date/Time"]).save()
	params = {
		'len' : len(Crime.objects.all())
	}
	return render(request, "DataEntry/dataEntry.html", params)