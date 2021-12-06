from django.shortcuts import render
from DataEntry.models import Crime

# Create your views here.
def dataInput(request):
	crimes = Crime.objects.all()

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
	return render(request, "Analysis/analysis.html", params)


def dashboard(request):
	return render(request, "Analysis/dashboard.html")