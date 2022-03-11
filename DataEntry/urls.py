from django.urls import path
from . import views

urlpatterns = [
	path('', views.dataEntry),
	path('speech2text', views.speech2text),
	path('text2analysis', views.text2analysis),
	path('save2db', views.save2db),
	path('dataupload', views.dataupload),
]