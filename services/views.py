from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm


from .models import *
# Create your views here.
def home(request):
    s = Service.objects.all()
    serv = {'serv':s} 
    return render(request,'home\home.html',serv)

# def about_us(request):
#     pass

# def contact_us(request):
#     pass

# def login(request):
#     pass

def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'home/signup.html', { 'form': form}) 
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')#profile info
        else:
            return render(request, 'home/signup.html', {'form': form})
        
def UserLoggedIn(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    return username

def logout_view(request):
    username = UserLoggedIn(request)
    if username != None:
        logout(request)
        return redirect('home')
    
# def settings(request):
#     pass

# def profile(request):
#     pass


