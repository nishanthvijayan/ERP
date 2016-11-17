from django.shortcuts import render, render_to_response,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.models import User, Group
from login.models import RegisterUserForm, EditUserForm, CreateGroupForm, EditGroupForm


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
	try:
		group = Group.objects.get(name=name)
	except Group.DoesNotExist:
		group = None
	if not group:
		return render_to_response('login/edit_group.html',{'message': 'Group \'' + name + '\' not found!'})
	else:
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
		elif task == 'add-user':
			if request.method == 'POST':
				username = request.POST.get('username')
				if not username:
					return render_to_response('login/edit_group.html',{'message': 'Some error occured', 'group_name': group.name})
				try:	
					user = User.objects.get(username=username)
				except User.DoesNotExist:
					user = None
				if user:
					group.user_set.add(user)
					return render_to_response('login/edit_group.html',{'message': 'User \'' + user.username + '\' added to the group \'' + group.name + '\' successfully.', 'group_name': group.name})
				else:
					return render_to_response('login/edit_group.html',{'message': 'User \'' + username + '\' not found!', 'group_name': group.name})
			else:
				pass
			c = {}
			c.update(csrf(request))
			c['group_name'] = group.name
			return render_to_response('login/edit_group.html',c)
		elif task == 'remove-user':
			if request.method == 'POST':
				username = request.POST.get('username')
				user = get_object_or_404(User, username=username)
				if user:
					user.groups.remove(group)
					return render_to_response('login/edit_group.html',{'message': 'User \'' + username + '\' successfully removed from the group \'' + group.name +'\'.', 'group_name': group.name})
				else:
					return render_to_response('login/edit_group.html',{'message': 'User \'' + username + '\' not found!', 'group_name': group.name})
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
			return HttpResponseRedirect('invalid')
	
	def get(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('home')
		c = {}
		c.update(csrf(request))
		return render_to_response('login/login.html',c)

class LogoutView(View):
	def get(self, request):
		auth.logout(request)
		return render_to_response("login/logout.html") 