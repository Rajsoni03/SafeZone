from django.shortcuts import render


# Create your views here.
def dataInput(request):
	return render(request, "Analysis/dataInput.html")


def dashboard(request):
	return render(request, "Analysis/dashboard.html")