from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from forms.models import WorkflowInstance, FormElementInstance, Workflow

@login_required
def workflow_instance_index(request, workflow_id): 
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    form_elements = workflow.form_elements.all()
    responses = workflow.instances.all()
    context = {'workflow': workflow, 'form_elements': form_elements, "responses": responses}
    return render(request, 'forms/workflow_instances/index.html', context)

@login_required
def workflow_instance_new(request, workflow_id): 
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    form_elements = workflow.form_elements.all()
    if request.method == 'POST':
        submission = WorkflowInstance(workflow_id=workflow_id, creator=request.user, current_state=workflow.initial_state())
        submission.save()
        for form_element in form_elements:
                submission.form_element_instances.create(form_element=form_element, value=request.POST[form_element.caption])
        # TODO: After collecting reponses the page should ideally redirect to a page listing current user's all submissions
        return redirect('forms:workflow-index')

    context = {'workflow': workflow, 'form_elements': form_elements}
    return render(request, 'forms/workflow_instances/new.html', context)
