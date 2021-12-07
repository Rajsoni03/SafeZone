from django.shortcuts import render
from DataEntry.models import Crime
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from django.utils.dateparse import parse_datetime
from math import sqrt
import pandas as pd
now = datetime.now()

# Create your views here.
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
		'time': "All",
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


def dataPoints(request):
	head 			= '{"type": "FeatureCollection","features": ['
	data_head 		= '{"type": "Feature", "properties": {'
	data_mid        = '},  "geometry": { "type": "Point", "coordinates": '
	data_tail 		= '} },'
	tail 			= ']}'

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	time 			= request.GET.get('time')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')
	fromDateTime	= request.GET.get('fromdatetime')
	toDateTime	 	= request.GET.get('todatetime')

	policeStation 	= None if policeStation == 'All' else policeStation
	circle 			= None if circle 		== 'All' else circle
	time 			= None if time 			== 'All' else time
	eventTypes 		= None if eventTypes 	== 'All' else eventTypes
	eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
	fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
	toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')

	fromDateTime 	= parse_datetime(fromDateTime)
	toDateTime 		= parse_datetime(toDateTime)

	print('\n All Points \n', policeStation, circle, time, eventTypes, eventSubTypes, '\n', fromDateTime, '\n', toDateTime, '\n\n')
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
	elif not policeStation and not circle and not eventTypes and not eventSubTypes: # 0000
		crimes = Crime.objects.all()

	lat_long = ''
	for crime in crimes:
		if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
			prop = f'"eventID" : "{crime.eventID}", "eventType" : "{crime.eventtype}", "eventSubType" : "{crime.eventsubtype}", "callerSource": "{crime.callerSource}", "datetime": "{crime.datetime}" '
			lat_long = lat_long + data_head + prop + data_mid + str([float(crime.longitude), float(crime.latitude)]) + data_tail
		

	data = head + lat_long + tail

	return JsonResponse(data=eval(data))

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

def getPrediction(request):
	# Hyper Parameters
	timeDelta		= request.GET.get('timeDelta')
	noOfPoints	 	= request.GET.get('noOfPoints')

	if timedelta != None and noOfPoints != None :

		# Get Request Data 
		policeStation 	= request.GET.get('policeStation')
		circle 			= request.GET.get('circle')
		time 			= request.GET.get('time')
		eventTypes 		= request.GET.get('eventTypes')
		eventSubTypes 	= request.GET.get('eventSubTypes')
		fromDateTime	= request.GET.get('fromdatetime')
		toDateTime	 	= request.GET.get('todatetime')

		# Handle Null values
		policeStation 	= None if policeStation == 'All' else policeStation
		circle 			= None if circle 		== 'All' else circle
		time 			= None if time 			== 'All' else time
		eventTypes 		= None if eventTypes 	== 'All' else eventTypes
		eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
		fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
		toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')

		fromDateTime 	= parse_datetime(fromDateTime)
		toDateTime 		= parse_datetime(toDateTime)

		print('\n Predictions \n', policeStation, circle, time, eventTypes, eventSubTypes, timeDelta, noOfPoints, '\n', fromDateTime, '\n', toDateTime, '\n\n')
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

		for i in crimes:
			DataDict["policeStation"].append(i.policeStation)
			DataDict["eventtype"].append(i.eventtype)
			DataDict["latitude"].append(float(i.latitude))
			DataDict["longitude"].append(float(i.longitude))
			DataDict["datetime"].append(i.datetime)
			DataDict["date"].append(i.datetime)
			DataDict["lat_long"].append(str(i.latitude)+","+str(i.longitude))

		df = pd.DataFrame(DataDict)
		df['hour'] 	= df['datetime'].dt.hour

		# Hyperparameters
		DIFF = 0.0011
		EX_DIFF = DIFF*2
		DAYS = int(timeDelta)
		NO_OF_POINTS = int(noOfPoints)
		Fw = 0.2
		Rw = 0.7
		Nw = 0.1
		LINES = 0.001
		todayDateTime = "2021-06-30T23:59:00"

		# Define Function for Calculating Points
		def CalculatePoint(latitude, longitude):
			# F = No. of crime at single point
			# R = No. of recent crime at single point
			# N = No. of crime in neabour points
			recent_time = parse_datetime(todayDateTime)-timedelta(days=DAYS)
			F = len(df.loc[(df["latitude"] == latitude) & df["longitude"] == longitude])
			R = len(df.loc[(df['latitude'] == latitude) & (df['longitude'] == longitude) & (df['date'] >= recent_time)])
			N = len(df.loc[(df['latitude'] > latitude-DIFF) & (df['latitude'] < latitude+DIFF) 
				& (df['longitude'] > longitude-DIFF) & (df['longitude'] < longitude+DIFF)])

			return (F*Fw) + (R*Rw)+ (N*Nw)


		# Create Dict for saving data output
		Prediction = {
			'points' : [], # F+R+N
		    'lat' : [], 
		    'long' : []
		}

		# Iterate over Unique Lat & Long Points
		# count = 0
		for l_l in df['lat_long'].unique():
			lat_long = [float(k) for k in l_l.split(',')]
			Prediction['points'].append(CalculatePoint(lat_long[0], lat_long[1]))
			Prediction['lat'].append(lat_long[0])
			Prediction['long'].append(lat_long[1])

			# count += 1
			# if count > 502:
			# 	break

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


