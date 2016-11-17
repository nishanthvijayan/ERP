from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.models import User, Group
from login.forms import RegisterUserForm, EditUserForm, CreateGroupForm, EditGroupForm
from django.contrib import messages

# After Login
def home(request):
	if request.user.is_authenticated():
		users = User.objects.all()
		groups = Group.objects.all()
		return render(request,'login/home.html', {'users': users, 'groups': groups})
	else:
		return HttpResponseRedirect('/')

# User - Management
def register_user(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = RegisterUserForm(data=request.POST)
		if form.is_valid():
			if form.save():
				messages.success(request, 'User \'' + form.cleaned_data['username'] + '\' successfully registered!')
			else:
				messages.error(request, 'Some error occured')
			return redirect('login:register-user')
	else:
		form = RegisterUserForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request, "login/register_user.html",args)

def remove_user(request,user_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	user = get_object_or_404(User, id=user_id)
	if user.delete():
		messages.success(request, 'User \'' + user.username + '\' successfully removed!')
	else:
		messages.error(request, 'Some error occured!')
	return redirect('login:login')

def edit_user(request,user_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	user = get_object_or_404(User, id=user_id)
	if request.method == 'POST':
		form = EditUserForm(request.POST, instance=user)
		if form.is_valid():
			if form.save():
				messages.success(request,'User \'' + user.username + '\' info successfully updated!')
			else:
				messages.error(request, 'Some error occured!')
			return redirect('login:edit-user',user_id)
	else:
		form = EditUserForm(instance=user)

	c = {}
	c.update(csrf(request))
	c['form'] = form
	c['user_id'] = user.id 
	c['username'] = user.username 
	return render(request, 'login/edit_user.html',c)

# Group Management
def create_group(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = CreateGroupForm(data=request.POST)
		if form.is_valid():
			if form.save():
				messages.success(request,'Group \'' + form.cleaned_data['name'] + '\' successfully created!')
			else:
				messages.error(request, 'Some error occured!')
			return redirect('login:create-group',user_id)
	else:
		form = CreateGroupForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request, "login/create_group.html",args)

def delete_group(request,group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, id=group_id)
	if group.delete():
		messages.success(request, 'Group \'' + group.name +'\' successfull deleted!')
	else:
		messages.error(request, 'Some error occured!')
	return redirect('login:home')


def show_group(request,group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, id=group_id)
	users = group.user_set.all()
	c = {}
	c.update(csrf(request))
	c['users'] = users
	c['group'] = group
	return render(request, 'login/show_group.html',c)

def edit_group_name(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, id=group_id)
	old_name = group.name
	if request.method == 'POST':
		form = EditGroupForm(request.POST,instance=group)
		if form.is_valid():
			if form.save():
				messages.success(request, 'Group name successfully changed form \'' + old_name + '\' to \'' + group.name + '\'.')
			else:
				messages.error(request, 'Some error occured!')
			return redirect('login:edit-group-name', group_id)
	else:
		form = EditGroupForm(instance=group)

	c = {}
	c.update(csrf(request))
	c['change_name_form'] = form
	c['group_id'] = group.id
	return render(request, 'login/edit_group_name.html',c)

def toggle_user_group(request,group_id):
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
	return redirect('login:show-group', group_id)


# LoginView
class LoginView(View):
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('home')
		else:
			c = {}
			c.update(csrf(request))
			c['message'] = 'Invalid Credentials. Please try again'
			return render(request, 'login/login.html',c)
	
	def get(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('home')
		c = {}
		c.update(csrf(request))
		return render(request, 'login/login.html',c)

class LogoutView(View):
	def get(self, request):
		auth.logout(request)
		c = {}
		c.update(csrf(request))
		c['message'] = 'You have successfully logged out.'
		return render(request, 'login/login.html',c) 
