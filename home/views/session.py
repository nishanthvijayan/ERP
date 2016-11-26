from django.shortcuts import render, redirect, resolve_url
from django.contrib import auth
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginView(View):

    '''
    Class to generate the login view.
    '''

    def post(self, request):
        '''
        View fuction for logging in the user.
        '''

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = resolve_url('/home/')

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            context = {
                'message': 'Invalid Credentials. Please try again', 'next': redirect_to}
            return render(request, 'home/login.html', context)

    def get(self, request):
        '''
        View fuction for displaying the dashboard of the user.
        '''

        if request.user.is_authenticated():
            return redirect('home:home')
        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        return render(request, 'home/login.html', {'next': redirect_to})


class HomeView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'home/index.html')


class LogoutView(View):

    '''
    Class to generate the logout view.
    '''

    def get(self, request):
        '''
        View fuction for logging out the user.
        '''

        auth.logout(request)
        context = {'message': 'You have successfully logged out.'}
        return render(request, 'home/login.html', context)
