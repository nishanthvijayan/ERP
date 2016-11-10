from django.shortcuts import render, get_object_or_404
from .models import Workflow

def index(request):
    return render(request, 'forms/workflows/index.html', {'workflows': Workflow.objects.all()})

def edit(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    return render(request, 'forms/workflows/edit.html', {'workflow': workflow})

def show(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    context = {'workflow': workflow,
     'states': workflow.state_set.all(),
      'transitions': workflow.transition_set.all(),
      'form_elements': workflow.formelement_set.all()}
    return render(request, 'forms/workflows/show.html', context)
