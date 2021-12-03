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
	for i in crimes:
		eventTypes.add(i.eventtype)
	eventSubTypes = set()
	for i in crimes:
		eventSubTypes.add(i.eventsubtype)
	params = {
		'totalCases': len(crimes),
		'center' : lat_long[0],
		'map_zoom' : 13,
		'policeStation' : 'All',
		'circle' : 'All',
		'todaysCases' : 0,
		'eventTypes' : list(eventTypes),
		'eventSubTypes' : list(eventSubTypes)

	}
	return render(request, "Map/map.html", params)

def dataPoints(request):
	head = '{"type": "FeatureCollection","features": ['
	tail = ']}'
	data_head = '{"geometry": { "type": "Point", "coordinates": '
	data_tail = '} },'

	crimes = Crime.objects.all()
	lat_long = ''

	for crime in crimes:
		lat_long = lat_long + data_head + str([float(crime.longitude), float(crime.latitude)]) + data_tail

	data = head + lat_long + tail
	return JsonResponse(data=eval(data))