from django.contrib import admin

from .models import Agent, Location, Address

admin.site.register(Agent)
admin.site.register(Location)
admin.site.register(Address)