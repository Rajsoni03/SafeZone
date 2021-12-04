from django.shortcuts import render
from DataEntry.models import Crime
from django.http import JsonResponse
from datetime import datetime
from django.utils.dateparse import parse_datetime
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
	tail 			= ']}'
	data_head 		= '{"type": "Feature", "geometry": { "type": "Point", "coordinates": '
	data_tail 		= '} },'

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

	print('\n\n', policeStation, circle, time, eventTypes, eventSubTypes, '\n', fromDateTime, '\n', toDateTime, '\n\n')
	crimes = Crime.objects.all()
 
	if policeStation and circle and eventTypes and eventSubTypes: # 1111
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif policeStation and circle and eventTypes and not eventSubTypes: # 1110
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventtype=eventTypes)
	elif policeStation and circle and not eventTypes and eventSubTypes: # 1101
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle, eventsubtype=eventSubTypes)
	elif policeStation and circle and not eventTypes and not eventSubTypes: # 1100
		crimes = Crime.objects.filter(policeStation=policeStation, circle=circle)

	if policeStation and not circle and eventTypes and eventSubTypes: # 1011
		crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif policeStation and not circle and eventTypes and not eventSubTypes: # 1010
		crimes = Crime.objects.filter(policeStation=policeStation, eventtype=eventTypes)
	elif policeStation and not circle and not eventTypes and eventSubTypes: # 1001
		crimes = Crime.objects.filter(policeStation=policeStation, eventsubtype=eventSubTypes)
	elif policeStation and not circle and not eventTypes and not eventSubTypes: # 1000
		crimes = Crime.objects.filter(policeStation=policeStation)

	if not policeStation and circle and eventTypes and eventSubTypes: # 0111
		crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes, eventsubtype=eventSubTypes)
	elif not policeStation and circle and eventTypes and not eventSubTypes: # 0110
		crimes = Crime.objects.filter(circle=circle, eventtype=eventTypes)
	elif not policeStation and circle and not eventTypes and eventSubTypes: # 0101
		crimes = Crime.objects.filter(circle=circle, eventsubtype=eventSubTypes)
	elif not policeStation and circle and not eventTypes and not eventSubTypes: # 0100
		crimes = Crime.objects.filter(circle=circle)

	if not policeStation and not circle and eventTypes and eventSubTypes: # 0011
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
			lat_long = lat_long + data_head + str([float(crime.longitude), float(crime.latitude)]) + data_tail

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
