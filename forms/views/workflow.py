from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from forms.models import Workflow
from forms.forms import WorkflowForm


@login_required
def workflow_index(request):
    '''
    Generates view for displaying list of all Workflow.
    '''

    return render(request, 'forms/workflows/index.html', {'workflows': Workflow.objects.all()})


@login_required
def workflow_show(request, workflow_id):
    '''
    Generates view for displaying a Workflow.
    '''

    workflow = get_object_or_404(Workflow, pk=workflow_id)
    context = {
        'workflow': workflow,
        'states': workflow.state_set.all(),
        'transitions': workflow.transition_set.all(),
        'form_elements': workflow.formelement_set.all()
    }
    return render(request, 'forms/workflows/show.html', context)


@login_required
def workflow_new(request):
    '''
    Generates view for creating a new Workflow.
    '''

    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forms:workflow-index')
    else:
        form = WorkflowForm()

    return render(request, 'forms/workflows/new.html', {'form': form})


@login_required
def workflow_edit(request, workflow_id):
    '''
    Generates view for editing a Workflow.
    '''

    workflow = get_object_or_404(Workflow, pk=workflow_id)
    if request.method == 'POST':
        form = WorkflowForm(request.POST, instance=workflow)
        if form.is_valid():
            form.save()
            return redirect('forms:workflow-index')
    else:
        form = WorkflowForm(
            {"name": workflow.name, "description": workflow.description})

    return render(request, 'forms/workflows/edit.html', {'form': form, 'workflow': workflow})


@login_required
def workflow_delete(request, workflow_id):
    '''
    Generates view for deleting a Workflow.
    '''

    workflow = get_object_or_404(Workflow, pk=workflow_id)
    workflow.delete()
    return redirect('forms:workflow-index')
