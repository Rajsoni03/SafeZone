from django.shortcuts import render
from DataEntry.models import Crime
from django.http import JsonResponse

# Create your views here.
def map(request):
	crimes = Crime.objects.all()
	lat_long = []
	long_sum = 0
	lat_sum = 0
	num = 0
	for crime in crimes:
		lat_long.append([float(crime.longitude), float(crime.latitude)])

		if num > 5:
			break
		num = num + 1
		long_sum = long_sum + float(crime.longitude)
		lat_sum = lat_sum + float(crime.latitude)

	total_len = len(lat_long)
	params = {
		'lat_long' : lat_long,
		# 'center' : [(long_sum/total_len), (lat_sum/total_len)],
		'center' : lat_long[0],
		'first_point': lat_long[-5],
		'map_zoom' : 13,
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