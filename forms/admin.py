from django.contrib import admin
from .models import Workflow, FormElement, FormElementListItem, State, Transition, WorkflowEntry, FormElementEntry

admin.site.register(Workflow)
admin.site.register(FormElement)
admin.site.register(FormElementListItem)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(WorkflowEntry)
admin.site.register(FormElementEntry)
