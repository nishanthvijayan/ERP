from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.models import User, Group

from home.forms import RegisterUserForm, EditUserForm, CreateGroupForm, EditGroupForm

# LoginView
class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home:home')
        else:
            context = {'message' : 'Invalid Credentials. Please try again'}
            return render(request, 'home/login.html', context)
    
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home:home')
        return render(request, 'home/login.html')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        context = {'message' : 'You have successfully logged out.'}
        return render(request, 'home/login.html', context) 

# After Login
def home(request):
    if request.user.is_authenticated():
        users = User.objects.all()
        return render(request, 'home/users/index.html', {'users': users})
    else:
        return redirect('home:login')

# User - Management
def user_register(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'User \'' + form.cleaned_data['username'] + '\' successfully registered!')
            else:
                messages.error(request, 'Some error occured')
            return redirect('home:user-register')
    else:
        form = RegisterUserForm()
    context = {'form' : form}
    return render(request, "home/users/new.html", context)

def user_edit(request, user_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            if form.save():
                messages.success(request,'User \'' + user.username + '\' info successfully updated!')
            else:
                messages.error(request, 'Some error occured!')
            return redirect('home:user-edit', user_id)
    else:
        form = EditUserForm(instance=user)
    context = {
            'form' : form,
            'user_id' : user.id,
            'username' : user.username
        }
    return render(request, 'home/users/edit.html', context)

def user_remove(request, user_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    user = get_object_or_404(User, id=user_id)
    if user.delete():
        messages.success(request, 'User \'' + user.username + '\' successfully removed!')
    else:
        messages.error(request, 'Some error occured!')
    return redirect('home:home')

# Group Management
def group_index(request):
    if request.user.is_authenticated():
        groups = Group.objects.all()
        return render(request, 'home/groups/index.html', {'groups': groups})
    else:
        return redirect('home:login')

def group_create(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    if request.method == 'POST':
        form = CreateGroupForm(data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request,'Group \'' + form.cleaned_data['name'] + '\' successfully created!')
            else:
                messages.error(request, 'Some error occured!')
            return redirect('home:group-create')
    else:
        form = CreateGroupForm()
    context = {'form' : form}
    return render(request, "home/groups/new.html", context)

def group_show(request, group_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    group = get_object_or_404(Group, id=group_id)
    users = group.user_set.all()
    context = {
            'users' : users,
            'group' : group
        }
    return render(request, 'home/groups/show.html', context)

def group_edit(request, group_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    group = get_object_or_404(Group, id=group_id)
    old_name = group.name
    if request.method == 'POST':
        form = EditGroupForm(request.POST, instance=group)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Group name successfully changed form \'' + old_name + '\' to \'' + group.name + '\'.')
            else:
                messages.error(request, 'Some error occured!')
            return redirect('home:group-edit', group_id)
    else:
        form = EditGroupForm(instance=group)

    context = {
            'change_name_form' : form,
            'group_id'         : group.id
        }
    return render(request, 'home/groups/edit.html', context)

def group_delete(request, group_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    group = get_object_or_404(Group, id=group_id)
    if group.delete():
        messages.success(request, 'Group \'' + group.name +'\' successfull deleted!')
    else:
        messages.error(request, 'Some error occured!')
    return redirect('home:home')

def group_user_toggle(request, group_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        group = get_object_or_404(Group, id=group_id)
        if user.groups.filter(name=group.name).count():
            user.groups.remove(group)
            messages.success(request, 'User \'' + user.username + '\' successfully removed from the group \'' + group.name +'\'.')
        else:
            group.user_set.add(user)
            messages.success(request, 'User \'' + user.username + '\' added to the group \'' + group.name + '\' successfully.')
    return redirect('home:group-show', group_id)
