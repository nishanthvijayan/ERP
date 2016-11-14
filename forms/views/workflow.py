from django.shortcuts import render, get_object_or_404, redirect
from forms.models import Workflow
from forms.forms import WorkflowForm

def workflow_index(request):
    return render(request, 'forms/workflows/index.html', {'workflows': Workflow.objects.all()})

def workflow_show(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    context = {'workflow': workflow,
     'states': workflow.state_set.all(),
      'transitions': workflow.transition_set.all(),
      'form_elements': workflow.formelement_set.all()}
    return render(request, 'forms/workflows/show.html', context)

def workflow_new(request):
    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            workflow = Workflow(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
            workflow.save()
            return render(request, 'forms/workflows/index.html', {'workflows': Workflow.objects.all()})
    else:
        form = WorkflowForm()

    return render(request, 'forms/workflows/new.html', {'form': form})

def workflow_edit(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            workflow.name = form.cleaned_data['name']
            workflow.description = form.cleaned_data['description']
            workflow.save()
            return render(request, 'forms/workflows/index.html', {'workflows': Workflow.objects.all()})
    else:
        form = WorkflowForm({"name": workflow.name, "description": workflow.description})

    return render(request, 'forms/workflows/edit.html', {'form': form, 'workflow': workflow})

def workflow_delete(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    workflow.delete()
    return redirect('forms:workflow-index')