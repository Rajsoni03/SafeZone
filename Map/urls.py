from django.urls import path
from . import views

urlpatterns = [
	path('', views.map),
	path('dataPoints/', views.dataPoints)
]