from django.shortcuts import render, get_object_or_404, redirect
from .models import Workflow, FormElement, State, Transition
from .forms import WorkflowForm, FormElementForm, StateForm, TransitionForm

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

def form_element_new(request, workflow_id):
    if request.method == 'POST':
        form = FormElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.workflow_id = workflow_id
            element.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = FormElementForm()

    return render(request, 'forms/form_elements/new.html', {'form': form, 'workflow_id': workflow_id})

def form_element_edit(request, workflow_id, element_id):
    element = get_object_or_404(FormElement, pk=element_id)
    if request.method == 'POST':
        form = FormElementForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            return redirect('forms:workflow-show', workflow_id)
    else:
        form = FormElementForm(instance=element)

    return render(request, 'forms/form_elements/edit.html', {'form': form, 'workflow_id': workflow_id, 'element_id': element_id})

def form_element_delete(request, workflow_id, element_id):
    element = get_object_or_404(FormElement, pk=element_id)
    element.delete()
    return redirect('forms:workflow-show', workflow_id)


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

def transition_delete(request, workflow_id, transition_id):
    transition = get_object_or_404(Transition, pk=transition_id)
    transition.delete()
    return redirect('forms:workflow-show', workflow_id)