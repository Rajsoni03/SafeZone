from django.urls import path
from . import views

urlpatterns = [
	path('', views.map),
	path('dataPoints/', views.dataPoints),
	path(r'^dataPoints/', views.dataPoints),
	path('getSubEvents/', views.getSubEvents),
	path(r'^getSubEvents/', views.getSubEvents),
	path('getPrediction/', views.getPrediction),
	path(r'^getPrediction/', views.getPrediction),
	path('getTopPrediction/', views.getTopPrediction),
	path(r'^getTopPrediction/', views.getTopPrediction),
	path('getNearPlaces/', views.getNearPlaces),
	path(r'^getNearPlaces/', views.getNearPlaces)
]