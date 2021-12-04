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
		'map_zoom' : 12,
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

# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "id": 5547245399530065,
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-92.88969665765762, 43.991089365322296]
#       },
#       "properties": {
#         "underground": "false",
#         "extrude": "true",
#         "height": 3,
#         "type": "building",
#         "min_height": 0,
#         "iso_3166_2": "US-MN",
#         "iso_3166_1": "US",
#         "tilequery": {
#           "distance": 155.91526196325026,
#           "geometry": "polygon",
#           "layer": "building"
#         }
#       }
#     },
#     {
#       "type": "Feature",
#       "id": 3017301441,
#       "geometry": {
#         "type": "Point",
#         "coordinates": [-92.89943173527718, 43.985390659777266]
#       },
#       "properties": {
#         "type": "service:driveway",
#         "structure": "none",
#         "oneway": "false",
#         "class": "service",
#         "iso_3166_2": "US-MN",
#         "len": 290,
#         "iso_3166_1": "US",
#         "tilequery": {
#           "distance": 849.4893375770641,
#           "geometry": "linestring",
#           "layer": "road"
#         }
#       }
#     }
#   ]
# }


def dataPoints(request):
	head 			= '{"type": "FeatureCollection","features": ['
	tail 			= ']}'
	data_head 		= '{"type": "Feature", "geometry": { "type": "Point", "coordinates": '
	data_tail 		= '},'
	prop_head 		= '},"properties": { '
	prop_tail  		= '}'

	policeStation 	= request.GET.get('policeStation')
	circle 			= request.GET.get('circle')
	time 			= request.GET.get('time')
	eventTypes 		= request.GET.get('eventTypes')
	eventSubTypes 	= request.GET.get('eventSubTypes')

	policeStation 	= None if policeStation == 'All' else policeStation
	circle 			= None if circle 		== 'All' else circle
	time 			= None if time 			== 'All' else time
	eventTypes 		= None if eventTypes 	== 'All' else eventTypes
	eventSubTypes 	= None if eventSubTypes == 'All' else eventSubTypes


	print('\n\n', policeStation, circle, time, eventTypes, eventSubTypes, '\n\n')

	crimes = Crime.objects.all()

	# 1111
	# 1110
	# 1101
	# 1100

	# 1011
	# 1010
	# 1001
	# 1000

	# 0111
	# 0110
	# 0101
	# 0100

	# 0011
	# 0010
	# 0001
	# 0000
 
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

		


	print(len(crimes))

	lat_long 		= ''
	for crime in crimes:
		lat_long = lat_long + data_head + str([float(crime.longitude), float(crime.latitude)]) +\
				   prop_head + f'"eventtype": "{crime.eventtype}", "eventsubtype": "{crime.eventsubtype}", "datetime": {crime.datetime}'+ prop_tail + data_tail

	data = head + lat_long + tail
	return JsonResponse(data=eval(data))


