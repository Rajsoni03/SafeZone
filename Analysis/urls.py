from django.urls import path
from . import views

urlpatterns = [
	path('', views.dataInput),
	path('dashboard/', views.dashboard),
	path('getData/', views.getData),
	path(r'^getData/', views.getData)
]