from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.models import Group

from forms.models import WorkflowEntry, Workflow, Transition, State


@login_required
def workflow_entry_admin_index(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    form_elements = workflow.formelement_set.all()

    response_list = workflow.workflowentry_set.all()
    page = request.GET.get('page')
    paginator = Paginator(response_list, 10)
    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        responses = paginator.page(1)
    except EmptyPage:
        responses = paginator.page(paginator.num_pages)

    context = {'workflow': workflow, 'form_elements': form_elements, "responses": responses}
    return render(request, 'forms/workflow_entries/admin_index.html', context)


@login_required
def workflow_entry_user_index(request):
    response_list = WorkflowEntry.objects.filter(creator=request.user)
    page = request.GET.get('page')
    paginator = Paginator(response_list, 5)
    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        responses = paginator.page(1)
    except EmptyPage:
        responses = paginator.page(paginator.num_pages)

    context = {"responses": responses, "responses_count": paginator.count}
    return render(request, 'forms/workflow_entries/user_index.html', context)


@login_required
def workflow_entry_new(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    if len(request.user.groups.filter(name=workflow.allowed_groups.values_list('name'))) == 0:
        return redirect('forms:workflow-index')

    workflow = get_object_or_404(Workflow, pk=workflow_id)
    form_elements = workflow.formelement_set.all()
    if request.method == 'POST':
        submission = WorkflowEntry(workflow_id=workflow_id, creator=request.user,
                                   current_state=workflow.initial_state())
        submission.save()
        for form_element in form_elements:
                submission.formelemententry_set.create(
                    form_element=form_element, value=request.POST[form_element.caption])

        return redirect('forms:workflow-entry-user-index')

    context = {'workflow': workflow, 'form_elements': form_elements}
    return render(request, 'forms/workflow_entries/new.html', context)


@login_required
def workflow_entry_pending_index(request):
    current_user_groups = request.user.groups.values_list('id', flat=True)

    # names of groups current user is not in
    bad_group_names = list(Group.objects.exclude(id__in=current_user_groups).values_list("name", flat=True))

    # States accessible by current user
    good_states = State.objects.exclude(
        allowed_groups__name__in=bad_group_names).filter(kind__in=['Initial', 'Intermediate'])

    response_list = WorkflowEntry.objects.filter(current_state__in=good_states)
    page = request.GET.get('page')
    paginator = Paginator(response_list, 5)
    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        responses = paginator.page(1)
    except EmptyPage:
        responses = paginator.page(paginator.num_pages)

    context = {"responses": responses, "responses_count": paginator.count}
    return render(request, 'forms/workflow_entries/pending_index.html', context)


@login_required
def workflow_entry_change_state(request):
    if request.method == 'POST':
        users_groups = request.user.groups.values_list("name", flat=True)
        workflow_entry_id = request.POST['workflow_entry_id']
        workflow_entry = get_object_or_404(WorkflowEntry, pk=workflow_entry_id)

        if len(workflow_entry.current_state.allowed_groups.filter(name__in=users_groups)) == 0:
            messages.error(request, 'You are not authorized to perform this action')
            return redirect('forms:workflow-entry-pending-index')

        transition_id = request.POST['transition_id']
        transition = get_object_or_404(Transition, pk=transition_id)
        workflow_entry.current_state = transition.to_state
        workflow_entry.save()

    return redirect('forms:workflow-entry-pending-index')
