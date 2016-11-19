from django.shortcuts import render, redirect, resolve_url
from django.contrib import auth
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = resolve_url('/users/')

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            context = {'message': 'Invalid Credentials. Please try again', 'next': redirect_to}
            return render(request, 'home/login.html', context)

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home:user-index')
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        return render(request, 'home/login.html', {'next': redirect_to})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        context = {'message': 'You have successfully logged out.'}
        return render(request, 'home/login.html', context)
