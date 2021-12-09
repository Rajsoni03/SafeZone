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

	for i in crimes:
		DataDict["policeStation"].append(i.policeStation)
		DataDict["eventType"].append(i.eventtype)
		DataDict["eventSubType"].append(i.eventsubtype)
		DataDict["datetime"].append(i.datetime)
		DataDict["circles"].append(i.circle)

	df = pd.DataFrame(DataDict)
	df['hour'] 	= df['datetime'].dt.hour
	df['date'] 	= df['datetime'].dt.date
	df['weekDay'] = df['datetime'].dt.dayofweek.map(dw_mapping)


	# Pi Chart Data (Top 10 Events Type)
	pi_data = {
	    'series': [i for i in df['eventType'].value_counts()[:10].values],
	    'labels': [str(i) for i in df['eventType'].value_counts()[:10].index],
	}
	print(pi_data['labels'])


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
		Monday.append(temp_df.Monday)
		Tuesday.append(temp_df.Tuesday)
		Wednesday.append(temp_df.Wednesday)
		Thursday.append(temp_df.Thursday)
		Friday.append(temp_df.Friday)
		Saturday.append(temp_df.Saturday)
		Sunday.append(temp_df.Sunday)

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
		temp_df = (df[df['eventType'] == i])['hour'].value_counts(normalize=True)
		hoursEvent_Type.append(i)    
		for i in hourEvent.keys():
			try:
				hourEvent[i].append(temp_df[i])
			except:
				hourEvent[i].append(0)

	print(hourEvent)


	params = {
		'totalCases': len(crimes),
		'policeStation' : 'All',
		'radius': "All",
		'circle' : 'All',
		'todaysCases' : 0,
		'eventTypes' : sorted(df['eventType'].unique()),
		'eventSubTypes' : sorted(df['eventSubType'].unique()),
		'policeStations' : sorted(df['policeStation'].unique()),
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
		'hoursEvent_Type':hoursEvent_Type

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

	policeStation 	= None if policeStation == 'All' else policeStation
	circle 			= None if circle 		== 'All' else circle
	radius 			= None if radius 		== 'All' else radius
	eventTypes 		= None if eventTypes 	== 'All' else eventTypes
	eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes
	fromDateTime	= "2021-04-01T00:00:00" if fromDateTime == None else (fromDateTime[:16] + ':00')
	toDateTime	 	= "2021-06-30T23:59:59" if toDateTime 	== None else (toDateTime[:16] + ':59')

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
	    'eventtype': [],
		'datetime': [],
	}

	for i in crimes:
		DataDict["policeStation"].append(i.policeStation)
		DataDict["eventtype"].append(i.eventtype)
		DataDict["datetime"].append(i.datetime)

	df = pd.DataFrame(DataDict)
	df['hour'] 	= df['datetime'].dt.hour
	df['weekDay'] = df['datetime'].dt.dayofweek.map(dw_mapping)


	# Pi Chart Data (Top 10 Events Type)
	pi_data = {
	    'series': [i for i in df['eventtype'].value_counts()[:10].values],
	    'labels': [i for i in df['eventtype'].value_counts()[:10].index],
	}

	print(pi_data)



	data = {
		'status' : True,
		'totalCases': len(crimes),
		# 'weeklyCrime': ,
		# 'dailyCrime': ,
		'pi_series': str([i for i in df['eventtype'].value_counts()[:10].values]),
	 	'pi_labels': str([i for i in df['eventtype'].value_counts()[:10].index])

	}
	return JsonResponse(data=data)