from django.shortcuts import render, get_object_or_404, redirect
from forms.models import FormElement
from forms.forms import FormElementForm

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