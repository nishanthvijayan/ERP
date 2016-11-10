from django.contrib import admin
from .models import Workflow, FormElement, FormElementListItem, State, Transition, WorkflowInstance, FormElementInstance

admin.site.register(Workflow)
admin.site.register(FormElement)
admin.site.register(FormElementListItem)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(WorkflowInstance)
admin.site.register(FormElementInstance)

