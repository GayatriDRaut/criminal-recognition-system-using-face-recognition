from django.contrib import admin

from .models import *
admin.site.register(User)

admin.site.register(ThiefLocation)
admin.site.register(Person)
admin.site.register(File)



