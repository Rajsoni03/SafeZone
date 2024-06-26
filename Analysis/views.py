from django.shortcuts import render
from DataEntry.models import Crime
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from django.utils.dateparse import parse_datetime
import pandas as pd

# Create your views here.
def dataInput(request):
	crimes = Crime.objects.all()

	fromDateTime = "2021-04-01T00:00:00"
	toDateTime = "2021-06-30T23:59:00"

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	radius 			= request.GET.get('radius')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')
	fromDateTime	= request.GET.get('fromdatetime')
	toDateTime	 	= request.GET.get('todatetime')
	timeOfevent	 	= request.GET.get('timeOfevent')

	policeStation 	= None if policeStation == 'All' else policeStation
	circle 			= None if circle 		== 'All' else circle
	radius 			= None if radius 		== 'All' else radius
	eventTypes 		= None if eventTypes 	== 'All' else eventTypes
	eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
	fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
	toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')
	timeOfevent 	= None if timeOfevent 	== 'All' else timeOfevent

	fromDateTime 	= parse_datetime(fromDateTime)
	toDateTime 		= parse_datetime(toDateTime)

	print('\n All Points \n', policeStation, circle, radius, eventTypes, eventSubTypes, '\n', fromDateTime, '\n', toDateTime, '\n\n')

	crimes = []

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


	# Convert data into Pandas DataFrame
	dw_mapping={
	    0: 'Monday', 
	    1: 'Tuesday', 
	    2: 'Wednesday', 
	    3: 'Thursday', 
	    4: 'Friday',
	    5: 'Saturday', 
	    6: 'Sunday'
	} 

	DataDict = {
		'policeStation':[],
	    'eventType': [],
	    'eventSubType': [],
		'datetime': [],
		'circles' : []
	}


	PS = {
		"PS1" : [26.835, 81.023],
		"PS2" : [26.850, 80.992],
		"PS3" : [26.900, 81.048],
		"PS4" : [26.865, 81.014]
	}

	if radius:
		radius = int(radius) * 0.005

	for crime in crimes:
		ThisLatitude = float(crime.latitude)
		ThisLongitude = float(crime.longitude)
		isRadius = True

		isTimeOfevent = True
		if timeOfevent:
			isTimeOfevent = False
			if int(timeOfevent) == int(str(crime.datetime).split(' ')[1][:2]):
				isTimeOfevent = True

		if isTimeOfevent:
			if radius:
				isRadius = False
				if policeStation is None:
					for ps in PS.keys():
						if (ThisLatitude >= PS[ps][0] - radius) and (ThisLongitude >= PS[ps][1] - radius) and (ThisLatitude <= PS[ps][0] + radius) and (ThisLongitude <= PS[ps][1] + radius):						
							if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
								DataDict["policeStation"].append(crime.policeStation)
								DataDict["eventType"].append(crime.eventtype)
								DataDict["eventSubType"].append(crime.eventsubtype)
								DataDict["datetime"].append(crime.datetime)
								DataDict["circles"].append(crime.circle)		
				else:
					if (ThisLatitude >= PS[policeStation][0] - radius) and (ThisLongitude >= PS[policeStation][1] - radius) and (ThisLatitude <= PS[policeStation][0] + radius) and (ThisLongitude <= PS[policeStation][1] + radius):
						if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
							DataDict["policeStation"].append(crime.policeStation)
							DataDict["eventType"].append(crime.eventtype)
							DataDict["eventSubType"].append(crime.eventsubtype)
							DataDict["datetime"].append(crime.datetime)
							DataDict["circles"].append(crime.circle)
			else:
				if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
					DataDict["policeStation"].append(crime.policeStation)
					DataDict["eventType"].append(crime.eventtype)
					DataDict["eventSubType"].append(crime.eventsubtype)
					DataDict["datetime"].append(crime.datetime)
					DataDict["circles"].append(crime.circle)

	df = pd.DataFrame(DataDict)
	df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H:%M:%S")
	df['hour'] 	= df['datetime'].dt.hour
	df['date'] 	= df['datetime'].dt.date
	df['weekDay'] = df['datetime'].dt.dayofweek.map(dw_mapping)


	# Pi Chart Data (Top 10 Events Type)
	pi_data = {
	    'series': [i for i in df['eventType'].value_counts()[:10].values],
	    'labels': [str(i) for i in df['eventType'].value_counts()[:10].index],
	}
	# print(pi_data['labels'])


	# lineAdwords chart data (datetime and cases)
	lineAdwords_data = {
		'data' : [i for i in df['date'].value_counts().values],
		'dates' : [str(i) for i in df['date'].value_counts().index]
	}

	# Hours Plot Data 
	hoursPlot = {
		'data':[i for i in df.sort_values(by=['hour'])['hour'].value_counts(sort=False).values],
		'cate':[i for i in df.sort_values(by=['hour'])['hour'].value_counts(sort=False).index]
	}

	# radialBar Plot data
	radialBar = {
		'series' : [i for i in df['weekDay'].value_counts(sort=False).values],
    	'labels' : [i for i in df['weekDay'].value_counts(sort=False).index],
	}

	# Week wise Events Graph
	Event_Type = []
	Monday = []
	Tuesday = []
	Wednesday = []
	Thursday = []
	Friday = []
	Saturday = []
	Sunday = []

	for i in df['eventType'].value_counts()[:10].index:
		temp_df = (df[df['eventType'] == i])['weekDay'].value_counts(normalize=True)
		Event_Type.append(i)
		try:
			Monday.append(temp_df.Monday)
			Tuesday.append(temp_df.Tuesday)
			Wednesday.append(temp_df.Wednesday)
			Thursday.append(temp_df.Thursday)
			Friday.append(temp_df.Friday)
			Saturday.append(temp_df.Saturday)
			Sunday.append(temp_df.Sunday)
		except Exception as e:
			print('\n', e, '\n')
		else:
			Monday.append(0)
			Tuesday.append(0)
			Wednesday.append(0)
			Thursday.append(0)
			Friday.append(0)
			Saturday.append(0)
			Sunday.append(0)

	weekEvent = {'Monday' : Monday,
				'Tuesday': Tuesday,  
				'Wednesday': Wednesday, 
				'Thursday': Thursday, 
				'Friday' : Friday, 
				'Saturday' : Saturday, 
				'Sunday' : Sunday,
				'index': Event_Type
				}

	# Hours wise Events Graph
	hoursEvent_Type = []
	hourEvent = {}
	for i in range(24):
		hourEvent[i] = []

	for i in df['eventType'].value_counts()[:10].index:
		temp_df = (df[df['eventType'] == i])['hour'].value_counts()#normalize=True
		hoursEvent_Type.append(i)    
		for i in hourEvent.keys():
			try:
				hourEvent[i].append(temp_df[i])
			except:
				hourEvent[i].append(0)


	params = {
		'totalCases': len(crimes),
		'timeOfevent' : timeOfevent if timeOfevent else "All",
		'policeStation' : policeStation if policeStation else 'All',
		'radius': radius if radius else 'All',
		'circle' : circle if circle else 'All',
		'todaysCases' : 0,
		'eventTypes' : sorted(df['eventType'].unique()),
		'eventSubTypes' : sorted(df['eventSubType'].unique()),
		'policeStations' : ['PS1', 'PS2', 'PS3', 'PS4'],
		'circles': sorted(df['circles'].unique()),
		'fromDateTime' : fromDateTime,
		'toDateTime' : toDateTime,
		'pi_series' : pi_data['series'],
		'pi_labels' : pi_data['labels'],
		'lineAdwords_data' : lineAdwords_data['data'],
		'lineAdwords_dates': lineAdwords_data['dates'],
		'hoursPlotData' : hoursPlot['data'],
		'hoursPlotCate': hoursPlot['cate'],
		'radialBarSeries':radialBar['series'],
		'radialBarLabels': radialBar['labels'],
		'WeekEventMonday' : weekEvent['Monday'],
		'WeekEventTuesday' : weekEvent['Tuesday'],
		'WeekEventWednesday' : weekEvent['Wednesday'],
		'WeekEventThursday' : weekEvent['Thursday'],
		'WeekEventFriday' : weekEvent['Friday'],
		'WeekEventSaturday' : weekEvent['Saturday'],
		'WeekEventSunday' : weekEvent['Sunday'],
		'WeekEventIndex': weekEvent['index'],
		'hourEvent' : hourEvent,
		'hoursEvent_Type':hoursEvent_Type,
		'monthCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=29)]),
		'weekCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=6)]),
		'dayCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=1)]),
		'fromDateTime' : str(fromDateTime).split(' ')[0]+'T'+str(fromDateTime).split(' ')[1],
		'toDateTime' : str(toDateTime).split(' ')[0]+'T'+str(toDateTime).split(' ')[1],

	}
	return render(request, "Analysis/analysis.html", params)


def dashboard(request):
	return render(request, "Analysis/dashboard.html")

def getData(request):

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	radius 			= request.GET.get('radius')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')
	fromDateTime	= request.GET.get('fromdatetime')
	toDateTime	 	= request.GET.get('todatetime')
	timeOfevent	 	= request.GET.get('timeOfevent')

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

	print('\n Json Points \n', policeStation, circle, radius, eventTypes, eventSubTypes, '\n', fromDateTime, '\n', toDateTime, '\n\n')

	crimes = []

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


	# Convert data into Pandas DataFrame
	dw_mapping={
	    0: 'Monday', 
	    1: 'Tuesday', 
	    2: 'Wednesday', 
	    3: 'Thursday', 
	    4: 'Friday',
	    5: 'Saturday', 
	    6: 'Sunday'
	} 

	DataDict = {
		'policeStation':[],
	    'eventtype': [],
		'datetime': [],
	}


	PS = {
		"PS1" : [26.835, 81.023],
		"PS2" : [26.850, 80.992],
		"PS3" : [26.900, 81.048],
		"PS4" : [26.865, 81.014]
	}

	if radius:
		radius = int(radius) * 0.005

	for crime in crimes:
		ThisLatitude = float(crime.latitude)
		ThisLongitude = float(crime.longitude)
		isRadius = True

		isTimeOfevent = True
		if timeOfevent:
			isTimeOfevent = False
			if int(timeOfevent) == int(str(crime.datetime).split(' ')[1][:2]):
				isTimeOfevent = True
		if isTimeOfevent:
			if radius:
				isRadius = False
				if policeStation is None:
					for ps in PS.keys():
						if (ThisLatitude >= PS[ps][0] - radius) and (ThisLongitude >= PS[ps][1] - radius) and (ThisLatitude <= PS[ps][0] + radius) and (ThisLongitude <= PS[ps][1] + radius):
							if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
								DataDict["policeStation"].append(crime.policeStation)
								DataDict["eventtype"].append(crime.eventtype)
								DataDict["datetime"].append(crime.datetime)
				else:
					if (ThisLatitude >= PS[policeStation][0] - radius) and (ThisLongitude >= PS[policeStation][1] - radius) and (ThisLatitude <= PS[policeStation][0] + radius) and (ThisLongitude <= PS[policeStation][1] + radius):
						if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
							DataDict["policeStation"].append(crime.policeStation)
							DataDict["eventtype"].append(crime.eventtype)
							DataDict["datetime"].append(crime.datetime)
			else:
				if crime.datetime >= fromDateTime and crime.datetime <= toDateTime:
					DataDict["policeStation"].append(crime.policeStation)
					DataDict["eventtype"].append(crime.eventtype)
					DataDict["datetime"].append(crime.datetime)
			

	df = pd.DataFrame(DataDict)
	df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H:%M:%S")
	df['hour'] 	= df['datetime'].dt.hour
	df['weekDay'] = df['datetime'].dt.dayofweek.map(dw_mapping)
	df['date'] = df['datetime'].dt.date


	# Pi Chart Data (Top 10 Events Type)
	pi_data = {
	    'series': [i for i in df['eventtype'].value_counts()[:10].values],
	    'labels': [i for i in df['eventtype'].value_counts()[:10].index],
	}

	
	data = {
		'status' : True,
		'totalCases': len(df),
		'monthCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=29)]),
		'weekCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=6)]),
		'dayCases': len(df[df['datetime'] >= parse_datetime('2021-06-30T23:59:59')-timedelta(days=1)]),
		'pi_series': str([i for i in df['eventtype'].value_counts()[:10].values]),
	 	'pi_labels': str([i for i in df['eventtype'].value_counts()[:10].index])

	}
	return JsonResponse(data=data)