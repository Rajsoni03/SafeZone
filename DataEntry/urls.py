from django.urls import path
from . import views

urlpatterns = [
	path('', views.dataEntry),
	path('speech2text', views.speech2text)
]