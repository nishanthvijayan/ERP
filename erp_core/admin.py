from django.contrib import admin
from .models import Employee, Department, Address, Pay


admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Address)
admin.site.register(Pay)
