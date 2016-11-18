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
				return render(request, 'login/register_user.html',{'message':'User \'' + form.cleaned_data['username'] + '\' successfully registered!'})
			else:
				return render(request, 'login/register_user.html',{'message': 'Some error occured'})
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
		return render(request, "login/remove_user.html",{'message': 'User \'' + user.username + '\' successfully removed!'})
	else:
		return render(request, 'login/remove_user.html',{'message': 'Some error occured'})

def edit_user(request,user_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	user = get_object_or_404(User, id=user_id)
	if request.method == 'POST':
		form = EditUserForm(request.POST, instance=user)
		if form.is_valid():
			if form.save():
				return render(request, "login/edit_user.html",{'message': 'User \'' + user.username + '\' info successfully updated!'})
			else:
				return render(request, 'login/edit_user.html',{'message': 'Some error occured'})
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
				return render(request, 'login/create_group.html',{'message':'Group \'' + form.cleaned_data['name'] + '\' successfully created!'})
			else:
				return render(request, 'login/create_group.html',{'message': 'Some error occured'})
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
		messages.success(request, 'Hello world.')
		return redirect('login:home')
	else:
		messages.error(request, 'Document deleted.')
		return render(request, 'login/home.html')


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

def edit_group(request, group_id, task):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	group = get_object_or_404(Group, id=group_id)
	old_name = group.name 
	# URL: /groups/{{ group_id }}/change-name
	if task == 'change-name':
		if request.method == 'POST':
			form = EditGroupForm(request.POST,instance=group)
			if form.is_valid():
				if form.save():
					return render(request,"login/edit_group.html",{'message': 'Group name successfully changed form \'' + old_name + '\' to \'' + group.name + '\'.', 'group_id': group.id})
				else:
					return render(request, 'login/edit_group.html',{'message': 'Some error occured'})
		else:
			form = EditGroupForm(instance=group)

		c = {}
		c.update(csrf(request))
		c['change_name_form'] = form
		c['group_id'] = group.id
		return render(request, 'login/edit_group.html',c)
	# URL: /edit_group/{{ group_name }}/add-user
	elif task == 'add-user':
		if request.method == 'POST':
			username = request.POST.get('username')
			user = get_object_or_404(User, username=username)
			group.user_set.add(user)
			return render(request, 'login/edit_group.html',{'message': 'User \'' + user.username + '\' added to the group \'' + group.name + '\' successfully.', 'group_id': group.id})
		else:
			pass
		c = {}
		c.update(csrf(request))
		c['group_id'] = group.id
		return render(request, 'login/edit_group.html',c)
	# URL: /edit_group/{{ group_name }}/remove-user
	elif task == 'remove-user':
		user_id = request.POST.get('user_id')
		print "USER : ", user_id
		user = get_object_or_404(User, id=user_id)
		user.groups.remove(group)
		return render(request, 'login/edit_group.html',{'message': 'User \'' + user.username + '\' successfully removed from the group \'' + group.name +'\'.', 'group_id': group.id})
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
