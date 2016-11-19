from django.shortcuts import render, redirect
from django.contrib import auth
from django.views import View

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
         return render(request, 'home/login.html')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        context = {'message' : 'You have successfully logged out.'}
        return render(request, 'home/login.html', context) 

