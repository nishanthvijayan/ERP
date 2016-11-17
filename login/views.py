from django.shortcuts import render, render_to_response,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.models import User, Group
from login.forms import RegisterUserForm, EditUserForm, CreateGroupForm, EditGroupForm


# After Login
def home(request):
	if request.user.is_authenticated():
		users = User.objects.all()
		groups = Group.objects.all()
		return render_to_response('login/home.html', {'users': users, 'groups': groups})
	else:
		HttpResponseRedirect('/')

def invalid(request):
	return render_to_response('login/invalid.html')


# User - Management
def register_user(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = RegisterUserForm(data=request.POST)
		if form.is_valid():
			if form.save():
				return render_to_response('login/register_user.html',{'message':'User \'' + form.cleaned_data['username'] + '\' successfully registered!'})
			else:
				return render_to_response('login/register_user.html',{'message': 'Some error occured'})
	else:
		form = RegisterUserForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response("login/register_user.html",args)

def remove_user(request,username):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	user = get_object_or_404(User, username=username)
	if user.delete():
		return render_to_response("login/remove_user.html",{'message': 'User \'' + username + '\' successfully removed!'})
	else:
		return render_to_response('login/remove_user.html',{'message': 'Some error occured'})

def edit_user(request,username):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	user = get_object_or_404(User, username=username)
	if request.method == 'POST':
		form = EditUserForm(request.POST, instance=user)
		if form.is_valid():
			if form.save():
				return render_to_response("login/edit_user.html",{'message': 'User \'' + username + '\' info successfully updated!'})
			else:
				return render_to_response('login/edit_user.html',{'message': 'Some error occured'})
	else:
		form = EditUserForm(instance=user)

	c = {}
	c.update(csrf(request))
	c['form'] = form
	c['username'] = user.username 
	return render_to_response('login/edit_user.html',c)

# Group Management
def create_group(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = CreateGroupForm(data=request.POST)
		if form.is_valid():
			if form.save():
				return render_to_response('login/create_group.html',{'message':'Group \'' + form.cleaned_data['name'] + '\' successfully created!'})
			else:
				return render_to_response('login/create_group.html',{'message': 'Some error occured'})
	else:
		form = CreateGroupForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render_to_response("login/create_group.html",args)

def delete_group(request,name):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, name=name)
	if group.delete():
		return render_to_response("login/delete_group.html",{'message': 'Group \'' + name + '\' successfully deleted!'})
	else:
		return render_to_response('login/delete_group.html',{'message': 'Some error occured'})


def show_group(request,name):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, name=name)
	users = group.user_set.all()
	c = {}
	c.update(csrf(request))
	c['users'] = users
	c['group'] = group
	return render_to_response('login/show_group.html',c)

def edit_group(request, name, task):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, name=name)
	# URL: /edit_group/{{ group_name }}/change-name
	if task == 'change-name':
		if request.method == 'POST':
			form = EditGroupForm(request.POST,instance=group)
			if form.is_valid():
				if form.save():
					return render_to_response("login/edit_group.html",{'message': 'Group name successfully changed form \'' + name + '\' to \'' + group.name + '\'.', 'group_name': group.name})
				else:
					return render_to_response('login/edit_group.html',{'message': 'Some error occured'})
		else:
			form = EditGroupForm(instance=group)

		c = {}
		c.update(csrf(request))
		c['change_name_form'] = form
		c['group_name'] = group.name
		return render_to_response('login/edit_group.html',c)
	# URL: /edit_group/{{ group_name }}/add-user
	elif task == 'add-user':
		if request.method == 'POST':
			username = request.POST.get('username')
			user = get_object_or_404(User, username=username)
			group.user_set.add(user)
			return render_to_response('login/edit_group.html',{'message': 'User \'' + user.username + '\' added to the group \'' + group.name + '\' successfully.', 'group_name': group.name})
		else:
			pass
		c = {}
		c.update(csrf(request))
		c['group_name'] = group.name
		return render_to_response('login/edit_group.html',c)
	# URL: /edit_group/{{ group_name }}/remove-user
	elif task == 'remove-user':
		username = request.POST.get('username')
		user = get_object_or_404(User, username=username)
		user.groups.remove(group)
		return render_to_response('login/edit_group.html',{'message': 'User \'' + username + '\' successfully removed from the group \'' + group.name +'\'.', 'group_name': group.name})
	else:
		return HttpResponseRedirect('/')

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
			return render_to_response('login/login.html',c)
	
	def get(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('home')
		c = {}
		c.update(csrf(request))
		return render_to_response('login/login.html',c)

class LogoutView(View):
	def get(self, request):
		auth.logout(request)
		c = {}
		c.update(csrf(request))
		c['message'] = 'You have successfully logged out.'
		return render_to_response('login/login.html',c) 
