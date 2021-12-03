from django.shortcuts import render
from DataEntry.models import Crime
from django.http import JsonResponse

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

	for i in crimes:
		eventTypes.add(i.eventtype)
		eventSubTypes.add(i.eventsubtype)
		policeStations.add(i.policeStation)
		circles.add(i.circle)

	params = {
		'totalCases': len(crimes),
		'center' : lat_long[0],
		'map_zoom' : 13,
		'policeStation' : 'All',
		'time': "All",
		'circle' : 'All',
		'todaysCases' : 0,
		'eventTypes' : sorted(list(eventTypes)),
		'eventSubTypes' : sorted(list(eventSubTypes)),
		'policeStations' : sorted(list(policeStations)),
		'circles': sorted(list(circles))

	}
	return render(request, "Map/map.html", params)

def dataPoints(request):
	head 			= '{"type": "FeatureCollection","features": ['
	tail 			= ']}'
	data_head 		= '{"geometry": { "type": "Point", "coordinates": '
	data_tail 		= '} },'

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	time 			= request.GET.get('time')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')

	crimes 			= Crime.objects.all()
	# policeStation=all&circle=all&time=all&eventTypes=all&eventSubTypes=all

	if policeStation is "all" or policeStation is None:
		crimes 			= Crime.objects.all()

	else:
		# print('\n\n', policeStation,'\n\n')
		crimes 		= Crime.objects.filter(policeStation = policeStation)

	
	lat_long 		= ''

	for crime in crimes:
		lat_long = lat_long + data_head + str([float(crime.longitude), float(crime.latitude)]) + data_tail

	data = head + lat_long + tail
	return JsonResponse(data=eval(data))