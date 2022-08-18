from django.shortcuts import render
from django.contrib.auth.models import auth, User

# Create your views here.
def main(request):
	return render(request, 'Main/index.html')

def login(request):
	if request.method == "POST":
		email = request.get("email", "").lower()
		password = request.get("password", "")

		user = auth.authenticate(username=email, password=password)
		print(user)

		if user is not None:
			auth.login(request, user)
			return render(request, 'Main/index.html')
		else:
			messages.info(request,'Email Does Not Exists')
			return render(request, 'Main/index.html')
	return render(request, 'Main/index.html')