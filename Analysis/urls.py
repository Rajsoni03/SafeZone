from django.urls import path 
from . import views

urlpatterns = [
	path('', views.dataInput),
	path(r'^', views.dataInput),
	path('dashboard/', views.dashboard),
	path('getData/', views.getData),
	path(r'^getData/', views.getData),
	path('getDataTest/', views.getDataTest),
	path(r'^getDataTest/', views.getDataTest),
	path('testPage/', views.testPage),
]