from django.shortcuts import render, redirect
from .forms import UserRegisterForm

#hello Tasya moy lubimyu

def index(request):
    return render(request, 'index.html', {'title': 'Главная страница'})
    
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            return redirect()
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form, 'title':'Регистрация'})

