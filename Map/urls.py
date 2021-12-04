from django.urls import path
from . import views

urlpatterns = [
	path('', views.map),
	path('dataPoints/', views.dataPoints),
	path(r'^dataPoints/', views.dataPoints),
	path('getSubEvents/', views.getSubEvents),
	path(r'^getSubEvents/', views.getSubEvents)
]