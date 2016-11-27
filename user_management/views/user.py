from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from user_management.forms import RegisterUserForm, EditUserForm


@login_required
def user_index(request):
    user_list = User.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user_management/users/index.html', {'users': users})


@login_required
def user_new(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'User \'' + form.cleaned_data['username'] + '\' successfully registered!')
            else:
                messages.error(request, 'Some error occured')
            return redirect('user-management:user-index')
    else:
        form = RegisterUserForm()
    context = {'form': form}
    return render(request, "user_management/users/new.html", context)


@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            if form.save():
                messages.success(request, 'User \'' + user.username + '\' info successfully updated!')
            else:
                messages.error(request, 'Some error occured!')
            # TODO: Once a user profile page is implemented, the redirect should lead there
            return redirect('user-management:user-index')
    else:
        form = EditUserForm(instance=user)
    context = {
            'form': form,
            'user_id': user.id,
            'username': user.username
        }
    return render(request, 'user_management/users/edit.html', context)


@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.delete():
        messages.success(request, 'User \'' + user.username + '\' successfully removed!')
    else:
        messages.error(request, 'Some error occured!')
    return redirect('user-management:user-index')
