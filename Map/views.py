from django.shortcuts import render
from DataEntry.models import Crime

# Create your views here.
def map(request):
	crimes = Crime.objects.all()
	lat_long = []
	long_sum = 0
	lat_sum = 0
	num = 0
	for crime in crimes:
		lat_long.append([float(crime.longitude), float(crime.latitude)])

		if num > 100:
			break
		num = num + 1
		long_sum = long_sum + float(crime.longitude)
		lat_sum = lat_sum + float(crime.latitude)

	total_len = len(lat_long)
	params = {
		'lat_long' : lat_long,
		# 'center' : [(long_sum/total_len), (lat_sum/total_len)],
		'center' : lat_long[0],
		'first_point': lat_long[-1],
		'map_zoom' : 11,
	}
	return render(request, "Map/map.html", params)