from django.shortcuts import render, get_object_or_404, redirect
from forms.models import State
from forms.forms import StateForm

def state_new(request, workflow_id):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.workflow_id = workflow_id
            state.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = StateForm()

    return render(request, 'forms/states/new.html', {'form': form, 'workflow_id': workflow_id})

def state_edit(request, workflow_id, state_id):
    state = get_object_or_404(State, pk=state_id)
    if request.method == 'POST':
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            form.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = StateForm(instance=state)

    return render(request, 'forms/states/edit.html', {'form': form, 'workflow_id': workflow_id, 'state_id': state_id})

def state_delete(request, workflow_id, state_id):
    state = get_object_or_404(State, pk=state_id)
    state.delete()
    return redirect('forms:workflow-show', workflow_id)
