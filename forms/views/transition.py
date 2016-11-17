from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from forms.models import Transition
from forms.forms import TransitionForm

@login_required
def transition_new(request, workflow_id):
    if request.method == 'POST':
        form = TransitionForm(request.POST)
        if form.is_valid():
            transition = form.save(commit=False)
            transition.workflow_id = workflow_id
            transition.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = TransitionForm()

    return render(request, 'forms/transitions/new.html', {'form': form, 'workflow_id': workflow_id})

@login_required
def transition_edit(request, workflow_id, transition_id):
    transition = get_object_or_404(Transition, pk=transition_id)
    if request.method == 'POST':
        form = TransitionForm(request.POST, instance=transition)
        if form.is_valid():
            form.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = TransitionForm(instance=transition)

    return render(request, 'forms/transitions/edit.html', {'form': form, 'workflow_id': workflow_id, 'transition_id': transition_id})

@login_required
def transition_delete(request, workflow_id, transition_id):
    transition = get_object_or_404(Transition, pk=transition_id)
    transition.delete()
    return redirect('forms:workflow-show', workflow_id)
