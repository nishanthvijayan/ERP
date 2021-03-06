from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from user_management.forms import GroupForm


@login_required
def group_index(request):
    group_list = Group.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(group_list, 10)
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(request, 'user_management/groups/index.html', {'groups': groups})


@login_required
def group_new(request):
    if request.method == 'POST':
        form = GroupForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Group \'' + form.cleaned_data['name'] + '\' successfully created!')
            else:
                messages.error(request, 'Some error occured!')
            return redirect('user-management:group-index')
    else:
        form = GroupForm()
    context = {'form': form}
    return render(request, "user_management/groups/new.html", context)


@login_required
def group_show(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user_list = group.user_set.all()
    page = request.GET.get('page')
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
            'users': users,
            'group': group
        }
    return render(request, 'user_management/groups/show.html', context)


@login_required
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    old_name = group.name
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Group name successfully changed form \'' +
                                 old_name + '\' to \'' + group.name + '\'.')
            else:
                messages.error(request, 'Some error occured!')
            return redirect('user-management:group-show', group_id)
    else:
        form = GroupForm(instance=group)

    context = {
            'change_name_form': form,
            'group_id': group.id
        }
    return render(request, 'user_management/groups/edit.html', context)


@login_required
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.delete():
        messages.success(request, 'Group \'' + group.name + '\' successfull deleted!')
    else:
        messages.error(request, 'Some error occured!')
    return redirect('user-management:group-index')


@login_required
def group_user_toggle(request, group_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        group = get_object_or_404(Group, id=group_id)
        if user.groups.filter(name=group.name).count():
            user.groups.remove(group)
            messages.success(request, 'User \'' + user.username +
                             '\' successfully removed from the group \'' + group.name + '\'.')
        else:
            group.user_set.add(user)
            messages.success(request, 'User \'' + user.username +
                             '\' added to the group \'' + group.name + '\' successfully.')
    return redirect('user-management:group-show', group_id)
