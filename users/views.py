from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Post, Comment

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

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта!")
    return redirect('index')

@ login_required
def profile_user(request):
    profile = request.user
    user_comments = Comment.objects.filter(author=profile, status="published").order_by("created_at")
    user_posts = Post.objects.filter(author=profile, status__in=["published, pending, draft"]).order_by("created_at")
    context = {
        "profile": profile,
        "title": f"Профиль {profile.username}",
        "comments": user_comments,
        "posts": user_posts,
    }
    return render(request, "users/profile.html", context)

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно изменён!")
            return redirect("users:profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "users/profile_edit.html", {"form": form, "title": "Редактирование профиля"})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменён!")
            return redirect("users:profile")
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'title': 'Смена пароля'
    }
    return render(request, 'users/change_password.html', context)
