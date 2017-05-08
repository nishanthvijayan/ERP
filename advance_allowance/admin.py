from django.contrib import admin

from .models.travel_allowance_advance.travel_allowance_advance import TravelAllowanceAdvance
from .models.travel_allowance_advance.travel_details import TravelDetails

admin.site.register(TravelAllowanceAdvance)
admin.site.register(TravelDetails)
