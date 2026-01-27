from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

#hello Tasya moy lubimyu

def index(request):
    return render(request, 'index.html', {'title': 'Главная страница SiL'})
    
def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form, 'title':'Регистрация'})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Авторизация прошла успешно!")
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form, 'title':'Авторизация'})

def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта!")
    return redirect('index')

def profile_user(request):
    pass