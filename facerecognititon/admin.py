from django.contrib import admin

from .models import *
admin.site.register(User)

admin.site.register(CriminalLastSpotted)
admin.site.register(Criminal)
admin.site.register(File)



