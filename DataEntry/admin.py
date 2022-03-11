from django.contrib import admin
from .models import Crime

# Register your models here.
class CrimeAdmin(admin.ModelAdmin):
    list_display=['id','eventID','district', 'policeStation', 'circle', 'eventtype', 'eventsubtype', 'latitude', 'longitude', 'datetime']
    # list_editable=[]
admin.site.register(Crime,CrimeAdmin)