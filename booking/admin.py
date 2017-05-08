from django.contrib import admin
from .models.mp_hall.mp_hall import MpHall
from .models.mp_hall.transition_history import TransitionHistory

# Register your models here.
admin.site.register(MpHall)
admin.site.register(TransitionHistory)
