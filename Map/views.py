from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from DataEntry.models import Crime
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from django.utils.dateparse import parse_datetime
from math import sin, cos, asin, sqrt, degrees, radians
import pandas as pd
import tensorflow as tf
import os
import requests

 
model = tf.keras.models.load_model(os.path.join(os.getcwd(), os.path.join('staticfiles','model.h5'))) # load .h5 Model
now = datetime.now()

Event_index = ['Accident', 'Accident Explosive', 'Animals Related', 'Animals Smugling',
				'Assault/Riot/Commotion', 'Attempted Murder', 'Child Crime',
				'Child Crime(Sexual Abuse)', 'Corona',
				'Crime On Phone Mobile Social Media Internet', 'Cyber Crimes',
				'Dacoity', 'Differently Abled People', 'Dispute', 'Domestic Violence',
				'Dowry Related Crime',
				'Election Offences-Violation Of Model Code Of Conduct', 'Encroachment',
				'Escort For Safety', 'Excise Act Offenses', 'Female Harrassment',
				'Female Sexual Harrassment', 'Forgery', 'Found Deadbody', 'Gambling',
				'Human Trafficking', 'Illegal Mining',
				'Information Against Other Government Departments',
				'Information Against Police', 'Kidnap', 'Major Fire', 'Medium Fire',
				'Missing', 'Murder', 'Ndps Act Offenses', 'Personally Threat',
				'Pick Pocket', 'Police Help Required By 108',
				'Police Help Required By 1090', 'Pollution', 'Property Disputes',
				'Robbery', 'Small Fire', 'Sos', 'Suicide', 'Suicide Attempt',
				'Suspicious Object Information', 'Suspicious Person Information',
				'Theft', 'Threat In Person', 'Threat On Phone Email Social Media',
				'Traffic Jam', 'Unclaimed Information', 'Unknown']

Event_index_top = ['Accident', 'Accident Explosive', 'Assault/Riot/Commotion',
				'Attempted Murder', 'Child Crime(Sexual Abuse)', 'Dacoity',
				'Female Harrassment', 'Female Sexual Harrassment', 'Found Deadbody',
				'Human Trafficking', 'Kidnap', 'Major Fire', 'Murder',
				'Police Help Required By 108', 'Robbery', 'Suicide',
				'Suspicious Object Information']



# Create your views here.
@login_required(login_url='/')
def map(request):
	crimes = Crime.objects.all()
	lat_long = []
	for crime in crimes:
		lat_long.append([float(crime.longitude), float(crime.latitude)])
		break

	eventTypes = set()
	eventSubTypes = set()
	policeStations = set()
	circles = set()

	fromDateTime = "2021-04-01T00:00:00"
	toDateTime = "2021-06-30T23:59:00"

	print(fromDateTime, toDateTime)

	for i in crimes:
		eventTypes.add(i.eventtype)
		eventSubTypes.add(i.eventsubtype)
		policeStations.add(i.policeStation)
		circles.add(i.circle)

	params = {
		'totalCases': len(crimes),
		'center' : lat_long[0],
		'map_zoom' : 12,
		'policeStation' : 'All',
		'radius': "All",
		'circle' : 'All',
		'todaysCases' : 0,
		'eventTypes' : sorted(list(eventTypes)),
		'eventSubTypes' : sorted(list(eventSubTypes)),
		'policeStations' : sorted(list(policeStations)),
		'circles': sorted(list(circles)),
		'fromDateTime' : fromDateTime,
		'toDateTime' : toDateTime

	}
	return render(request, "Map/map.html", params)


@login_required(login_url='/')
def dataPoints(request):
	head 			= '{"type": "FeatureCollection","features": ['
	data_head 		= '{"type": "Feature", "properties": {'
	data_mid        = '},  "geometry": { "type": "Point", "coordinates": '
	data_tail 		= '} },'
	tail 			= ']}'

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	radius 			= request.GET.get('radius')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')
	timeOfevent	 	= request.GET.get('timeOfevent')
	fromDateTime	= request.GET.get('fromdatetime')
	toDateTime	 	= request.GET.get('todatetime')

	policeStation 	= None if policeStation == 'All' else policeStation
	circle 			= None if circle 		== 'All' else circle
	radius 			= None if radius 		== 'All' else radius
	eventTypes 		= None if eventTypes 	== 'All' else eventTypes
	eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
	timeOfevent 	= None if timeOfevent 	== 'All' else timeOfevent
	fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
	toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')

	fromDateTime 	= parse_datetime(fromDateTime)
	toDateTime 		= parse_datetime(toDateTime)

	print('\n All Points \n', policeStation, circle, radius, eventTypes, eventSubTypes, '\n', fromDateTime, '\n', toDateTime, '\n\n')
	crimes = Crime.objects.all()
 
	if policeStation and circle and eventTypes and eventSubTypes: # 1111
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif policeStation and circle and eventTypes and not eventSubTypes: # 1110
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes)
	elif policeStation and circle and not eventTypes and eventSubTypes: # 1101
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventsubtype=eventSubTypes)
	elif policeStation and circle and not eventTypes and not eventSubTypes: # 1100
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle)

	elif policeStation and not circle and eventTypes and eventSubTypes: # 1011
		crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif policeStation and not circle and eventTypes and not eventSubTypes: # 1010
		crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes)
	elif policeStation and not circle and not eventTypes and eventSubTypes: # 1001
		crimes = Crime.objects.filter(policeStation=policeStation, eventsubtype=eventSubTypes)
	elif policeStation and not circle and not eventTypes and not eventSubTypes: # 1000
		crimes = Crime.objects.filter(policeStation=policeStation)

	elif not policeStation and circle and eventTypes and eventSubTypes: # 0111
		crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif not policeStation and circle and eventTypes and not eventSubTypes: # 0110
		crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes)
	elif not policeStation and circle and not eventTypes and eventSubTypes: # 0101
		crimes = Crime.objects.filter(circle=circle, eventsubtype=eventSubTypes)
	elif not policeStation and circle and not eventTypes and not eventSubTypes: # 0100
		crimes = Crime.objects.filter(circle=circle)

	elif not policeStation and not circle and eventTypes and eventSubTypes: # 0011
		crimes = Crime.objects.filter(eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif not policeStation and not circle and eventTypes and not eventSubTypes: # 0010
		crimes = Crime.objects.filter(eventtype=eventTypes)
	elif not policeStation and not circle and not eventTypes and eventSubTypes: # 0001
		crimes = Crime.objects.filter(eventsubtype=eventSubTypes)
	# elif not policeStation and not circle and not eventTypes and not eventSubTypes: # 0000
	# 	crimes = Crime.objects.all()

	PS = {
		"PS1" : [26.835, 81.023],
		"PS2" : [26.850, 80.992],
		"PS3" : [26.900, 81.048],
		"PS4" : [26.865, 81.014]
	}

	if radius:
		radius = int(radius) * 0.005

	lat_long = ''
	for crime in crimes:
		ThisLatitude = float(crime.latitude)
		ThisLongitude = float(crime.longitude)
		isRadius = True
		if radius:
			isRadius = False
			if policeStation is None:
				for ps in PS.keys():
					if (ThisLatitude >= PS[ps][0] - radius) and (ThisLongitude >= PS[ps][1] - radius) and (ThisLatitude <= PS[ps][0] + radius) and (ThisLongitude <= PS[ps][1] + radius):
						isRadius = True				
			else:
				if (ThisLatitude >= PS[policeStation][0] - radius) and (ThisLongitude >= PS[policeStation][1] - radius) and (ThisLatitude <= PS[policeStation][0] + radius) and (ThisLongitude <= PS[policeStation][1] + radius):
						isRadius = True				

		isTimeOfevent = True
		if timeOfevent:
			isTimeOfevent = False
			if int(timeOfevent) == int(str(crime.datetime).split(' ')[1][:2]):
				isTimeOfevent = True

		if crime.datetime >= fromDateTime and crime.datetime <= toDateTime and isRadius and isTimeOfevent:
			prop = f'"eventID" : "{crime.eventID}", "eventType" : "{crime.eventtype}", "eventSubType" : "{crime.eventsubtype}", "callerSource": "{crime.callerSource}", "datetime": "{crime.datetime}" '
			lat_long = lat_long + data_head + prop + data_mid + str([ThisLongitude, ThisLatitude]) + data_tail
		

	data = head + lat_long + tail

	return JsonResponse(data=eval(data))


@login_required(login_url='/')
def getSubEvents(request):
	eventTypes 		= request.GET.get('eventTypes')
	eventTypes 		= None if eventTypes == 'All' else eventTypes

	crimes = Crime.objects.filter(eventtype=eventTypes) if eventTypes else Crime.objects.all()
	
	eventSubTypes = set()
	for i in crimes:
		eventSubTypes.add(i.eventsubtype)

	print(len(eventSubTypes))
	data = {
		'status' : True,
		'eventSubTypes' : list(eventSubTypes)
	}
	return JsonResponse(data=data)


@login_required(login_url='/')
def getPrediction(request):
	# Hyper Parameters
	timeDelta			= request.GET.get('timeDelta')
	noOfPoints	 		= request.GET.get('noOfPoints')
	timeOfpatrolling	= request.GET.get('timeOfpatrolling')
	weekDay	 			= request.GET.get('weekDay')	

	if timedelta != None and noOfPoints != None and timeOfpatrolling != None:

		# Get Request Data 
		policeStation 	= request.GET.get('policeStation')
		circle 			= request.GET.get('circle')
		radius 			= request.GET.get('radius')
		eventTypes 		= request.GET.get('eventTypes')
		eventSubTypes 	= request.GET.get('eventSubTypes')
		fromDateTime	= request.GET.get('fromdatetime')
		toDateTime	 	= request.GET.get('todatetime')

		# Handle Null values
		policeStation 	= None if policeStation == 'All' else policeStation
		circle 			= None if circle 		== 'All' else circle
		radius 			= 100  if radius 		== 'All' else radius
		eventTypes 		= None if eventTypes 	== 'All' else eventTypes
		eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
		fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
		toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')

		fromDateTime 	= parse_datetime(fromDateTime)
		toDateTime 		= parse_datetime(toDateTime)

		# Apply Classification Model
		timeOfpatrolling = int(timeOfpatrolling)
		weekDay = int(weekDay)

		if policeStation == "PS1":
			PS1, PS2, PS3, PS4 = 1,0,0,0
		elif policeStation == "PS2":
			PS1, PS2, PS3, PS4 = 0,1,0,0
		elif policeStation == "PS3":
			PS1, PS2, PS3, PS4 = 0,0,1,0
		elif policeStation == "PS4":
			PS1, PS2, PS3, PS4 = 0,0,0,1
		elif policeStation == None:
			PS1, PS2, PS3, PS4 = 0,0,0,0

		# Predict top 3 Event Type
		predictedEvent = model.predict([[timeOfpatrolling, timeOfpatrolling, weekDay, PS1, PS2, PS3, PS4]])
		predictedEventIndex = pd.DataFrame({'predictions':predictedEvent[0]}).sort_values('predictions', ascending=False).index

		top_predicted_events = []
		top_predicted_events_weights = []
		for n_event in range(3):
			top_predicted_events.append(Event_index[predictedEventIndex[n_event]])
			top_predicted_events_weights.append(predictedEvent[0][predictedEventIndex[n_event]])
			print("Event Type:", Event_index[predictedEventIndex[n_event]], "\nProbability:", predictedEvent[0][predictedEventIndex[n_event]], '\n')

		print('\n Predictions \n', policeStation, circle, radius, eventTypes, eventSubTypes, timeDelta, noOfPoints, '\n', fromDateTime, '\n', toDateTime, '\n\n')
		crimes = Crime.objects.all()
	 
		if policeStation and circle and eventTypes and eventSubTypes: # 1111
			crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
		elif policeStation and circle and eventTypes and not eventSubTypes: # 1110
			crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes)
		elif policeStation and circle and not eventTypes and eventSubTypes: # 1101
			crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventsubtype=eventSubTypes)
		elif policeStation and circle and not eventTypes and not eventSubTypes: # 1100
			crimes = Crime.objects.filter(policeStation=policeStation, circle=circle)

		elif policeStation and not circle and eventTypes and eventSubTypes: # 1011
			crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes, eventsubtype=eventSubTypes)
		elif policeStation and not circle and eventTypes and not eventSubTypes: # 1010
			crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes)
		elif policeStation and not circle and not eventTypes and eventSubTypes: # 1001
			crimes = Crime.objects.filter(policeStation=policeStation, eventsubtype=eventSubTypes)
		elif policeStation and not circle and not eventTypes and not eventSubTypes: # 1000
			crimes = Crime.objects.filter(policeStation=policeStation)

		elif not policeStation and circle and eventTypes and eventSubTypes: # 0111
			crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
		elif not policeStation and circle and eventTypes and not eventSubTypes: # 0110
			crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes)
		elif not policeStation and circle and not eventTypes and eventSubTypes: # 0101
			crimes = Crime.objects.filter(circle=circle, eventsubtype=eventSubTypes)
		elif not policeStation and circle and not eventTypes and not eventSubTypes: # 0100
			crimes = Crime.objects.filter(circle=circle)

		elif not policeStation and not circle and eventTypes and eventSubTypes: # 0011
			crimes = Crime.objects.filter(eventtype=eventTypes, eventsubtype=eventSubTypes)
		elif not policeStation and not circle and eventTypes and not eventSubTypes: # 0010
			crimes = Crime.objects.filter(eventtype=eventTypes)
		elif not policeStation and not circle and not eventTypes and eventSubTypes: # 0001
			crimes = Crime.objects.filter(eventsubtype=eventSubTypes)
		# elif not policeStation and not circle and not eventTypes and not eventSubTypes: # 0000
		# 	crimes = Crime.objects.all()

		# Create Pandas DataFrame For Faster Filtering
		DataDict = {
			'policeStation':[],
		    'eventtype': [],
			'latitude': [], 
		    'longitude': [],
			'datetime': [],
			'date':[],
			'lat_long': []
		}

		# for evnt in top_predicted_events:
		# 	# Fatch and Filtering data
		# 	if policeStation and circle:
		# 		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=evnt)
		# 	elif not policeStation and circle: 
		# 		crimes = Crime.objects.filter(circle=circle, eventtype=evnt)
		# 	elif policeStation and not circle:
		# 		crimes = Crime.objects.filter(policeStation=policeStation, eventtype=evnt)
		# 	elif not policeStation and not circle : 
		# 		crimes = Crime.objects.filter(eventtype=evnt)

		PS = {
			"PS1" : [26.835, 81.023],
			"PS2" : [26.850, 80.992],
			"PS3" : [26.900, 81.048],
			"PS4" : [26.865, 81.014]
		}

		radius = int(radius) * 0.005

		# add to df_dict
		for crime in crimes:
			if crime.eventtype == 'Dispute':
				continue
			ThisLatitude = float(crime.latitude)
			ThisLongitude = float(crime.longitude)

			if policeStation is None:
				for ps in PS.keys():
					if (ThisLatitude >= PS[ps][0] - radius) and (ThisLongitude >= PS[ps][1] - radius) and (ThisLatitude <= PS[ps][0] + radius) and (ThisLongitude <= PS[ps][1] + radius):
						DataDict["policeStation"].append(crime.policeStation)
						DataDict["eventtype"].append(crime.eventtype)
						DataDict["latitude"].append(ThisLatitude)
						DataDict["longitude"].append(ThisLongitude)
						DataDict["datetime"].append(crime.datetime)
						DataDict["date"].append(crime.datetime)
						DataDict["lat_long"].append(str(crime.latitude)+","+str(crime.longitude))			
			else:
				if (ThisLatitude >= PS[policeStation][0] - radius) and (ThisLongitude >= PS[policeStation][1] - radius) and (ThisLatitude <= PS[policeStation][0] + radius) and (ThisLongitude <= PS[policeStation][1] + radius):
					DataDict["policeStation"].append(crime.policeStation)
					DataDict["eventtype"].append(crime.eventtype)
					DataDict["latitude"].append(ThisLatitude)
					DataDict["longitude"].append(ThisLongitude)
					DataDict["datetime"].append(crime.datetime)
					DataDict["date"].append(crime.datetime)
					DataDict["lat_long"].append(str(crime.latitude)+","+str(crime.longitude))

		df = pd.DataFrame(DataDict)
		df['hour'] = df['datetime'].dt.hour

		# Hyperparameters
		DIFF = 0.0011
		EX_DIFF = DIFF*2
		DAYS = int(timeDelta)
		NO_OF_POINTS = int(noOfPoints)
		Fw = 0.2
		Rw = 0.7
		Nw = 0.1
		Ew = 1000
		LINES = 0.002
		todayDateTime = "2021-06-30T23:59:00"

		# Define Function for Calculating Points
		def CalculatePoint(latitude, longitude):
			# F = No. of crime at single point
			# R = No. of recent crime at single point
			# N = No. of crime in neabour points
			recent_time = parse_datetime(todayDateTime)-timedelta(days=DAYS)
			E1 = len(df.loc[(df["eventtype"] == top_predicted_events[0])])
			E2 = len(df.loc[(df["eventtype"] == top_predicted_events[1])])
			E3 = len(df.loc[(df["eventtype"] == top_predicted_events[2])])

			F = len(df.loc[(df["latitude"] == latitude) & (df["longitude"] == longitude) & (df["hour"] >= timeOfpatrolling-2) & (df["hour"] <= timeOfpatrolling+2)])
			R = len(df.loc[(df['latitude'] == latitude) & (df['longitude'] == longitude) & (df['date'] >= recent_time) & (df["hour"] >= timeOfpatrolling-2) & (df["hour"] <= timeOfpatrolling+2)])
			N = len(df.loc[(df['latitude'] > latitude-DIFF) & (df['latitude'] < latitude+DIFF) 
				& (df['longitude'] > longitude-DIFF) & (df['longitude'] < longitude+DIFF) & (df["hour"] >= timeOfpatrolling-2) & (df["hour"] <= timeOfpatrolling+2)])

			E = E1 * top_predicted_events_weights[0] + E2 * top_predicted_events_weights[1] + E3 * top_predicted_events_weights[2]
			return (F*Fw) + (R*Rw)+ (N*Nw) + (E*Ew)

		# Create Dict for saving data output
		Prediction = {
			'points' : [], # F+R+N
		    'lat' : [], 
		    'long' : []
		}

		# Iterate over Unique Lat & Long Points
		for l_l in df['lat_long'].unique():
			lat_long = [float(k) for k in l_l.split(',')]
			Prediction['points'].append(CalculatePoint(lat_long[0], lat_long[1]))
			Prediction['lat'].append(lat_long[0])
			Prediction['long'].append(lat_long[1])


		# Convert Prediction Dict to DataFrame & Sort by points
		points_df = pd.DataFrame(Prediction)
		points_df = points_df.sort_values(by='points', ascending=False)
		points_df = points_df.reset_index(drop=True)
		points_df = points_df.reset_index()


		for i in points_df.values:
		    indexs = points_df.loc[(points_df['lat'] > i[2]-EX_DIFF) & (points_df['lat'] < i[2]+EX_DIFF) 
		                            & (points_df['long'] > i[3]-EX_DIFF) & (points_df['long'] < i[3]+EX_DIFF) 
		                            & (points_df['index'] > int(i[0]))
		                           ].index
		    points_df.drop(indexs, inplace = True)

		points_df = points_df.iloc[:,1:].reset_index(drop=True)
		points_df = points_df.reset_index()
		points_df = points_df.iloc[:NO_OF_POINTS,:]

		# Create Geo Json Data 
		data_str = ''
		for data_points in points_df.values:
			prop = f'"point" : "{data_points[1]}", "color": "#F7455D"'

			lineLatLong = f'[[{(data_points[3])}, {(data_points[2])}],\
							 [{(data_points[3])-LINES}, {(data_points[2])-LINES}], [{(data_points[3])+LINES}, {(data_points[2])-LINES}], \
							 [{(data_points[3])+LINES}, {(data_points[2])+LINES}], [{(data_points[3])-LINES}, {(data_points[2])+LINES}], \
							 [{(data_points[3])-LINES}, {(data_points[2])-LINES}], [{(data_points[3])+LINES}, {(data_points[2])-LINES}], \
							 [{(data_points[3])-LINES}, {(data_points[2])+LINES}], [{(data_points[3])+LINES}, {(data_points[2])+LINES}],\
							 [{(data_points[3])}, {(data_points[2])}],\
							 ]'

			linePlot = '"geometry": {"type": "LineString", "coordinates": ' + lineLatLong + ' },'
			pointGeo = '"geometry": { "type": "Point", "coordinates": ' + str([data_points[3], data_points[2]]) + '},'

			data_str = data_str + '{"type": "Feature", "properties": {' + prop + '},' + linePlot + '},'
			
		data = '{"type": "FeatureCollection","features": [' + data_str + ']}'

		return JsonResponse(data=eval(data))


	else:	
		print('\n\n there is no Predictions \n\n')
		data = '{"type": "FeatureCollection","features": []}'
		return JsonResponse(data=eval(data))


@login_required(login_url='/')
def getTopPrediction(request):

	# Get Request Data 
	policeStation 		= request.GET.get('policeStation')
	timeOfpatrolling	= int(request.GET.get('timeOfpatrolling'))
	weekDay	 			= int(request.GET.get('weekDay'))	

	policeStation 	= None if policeStation == 'All' else policeStation

	if policeStation == "PS1":
		PS1, PS2, PS3, PS4 = 1,0,0,0
	elif policeStation == "PS2":
		PS1, PS2, PS3, PS4 = 0,1,0,0
	elif policeStation == "PS3":
		PS1, PS2, PS3, PS4 = 0,0,1,0
	elif policeStation == "PS4":
		PS1, PS2, PS3, PS4 = 0,0,0,1
	elif policeStation == None:
		PS1, PS2, PS3, PS4 = 0,0,0,0

	# Apply Classification Model
	# Predict top 3 Event Type
	predictedEvent = model.predict([[timeOfpatrolling, timeOfpatrolling, weekDay, PS1, PS2, PS3, PS4]])
	predictedEventIndex = pd.DataFrame({'predictions':predictedEvent[0]}).sort_values('predictions', ascending=False).index

	top_predicted_events = []
	top_predicted_events_weights = []
	for n_event in range(5):
		top_predicted_events.append(Event_index[predictedEventIndex[n_event]])
		top_predicted_events_weights.append(str(predictedEvent[0][predictedEventIndex[n_event]]))
		print("Event Type:", Event_index[predictedEventIndex[n_event]], "\nProbability:", predictedEvent[0][predictedEventIndex[n_event]], '\n')


	data = {
		"predicted_events": top_predicted_events,
		"predicted_events_weights":	top_predicted_events_weights
	}
	return JsonResponse(data=data)

def getNearPlaces(request):
# 	lat = 26.876
# 	long = 81.055
# 	limit = 50

# 	url = "https://api.foursquare.com/v3/places/nearby?ll={}%2C{}&limit={}".format(lat, long, limit)

# 	headers = {
# 	    "Accept": "application/json",
# 	    "Authorization": "fsq3AJY1p0lkNo9/6QWGrb7R1nZANvJeGz3EOnG9e8g39lA="
# 	}

# 	response = requests.request("GET", url, headers=headers)
# 	data = json.loads(json.dumps(json.JSONDecoder().raw_decode(response.text)))

# 	list_data = data[0]['results']

# 	data = {
# 		'categories' : [],
# 		'name' : [],
# 		'distance' : []
# 	}

# 	for i in list_data:
# 	    try:
# 	        categories = i['categories'][0]['name']
# 	        name = i['name']
# 	        distance = i['distance']
			
# 			data['categories'] = 
# 			data['name'] = 
# 			data['distance'] = 
# 	    except:
# 	        pass

	
	params = {
		'status' : True,
	}
	return JsonResponse(params)
