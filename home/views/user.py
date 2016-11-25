from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from home.forms import RegisterUserForm, EditUserForm


@login_required
def user_index(request):
    users = User.objects.all()
    return render(request, 'home/users/index.html', {'users': users})


@login_required
def user_new(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'User \'' + form.cleaned_data['username'] + '\' successfully registered!')
            else:
                messages.error(request, 'Some error occured')
            return redirect('home:user-index')
    else:
        form = RegisterUserForm()
    context = {'form': form}
    return render(request, "home/users/new.html", context)


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
            return redirect('home:user-index')
    else:
        form = EditUserForm(instance=user)
    context = {
            'form': form,
            'user_id': user.id,
            'username': user.username
        }
    return render(request, 'home/users/edit.html', context)


@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.delete():
        messages.success(request, 'User \'' + user.username + '\' successfully removed!')
    else:
        messages.error(request, 'Some error occured!')
    return redirect('home:user-index')
