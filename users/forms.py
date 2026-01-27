from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования профиля"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
