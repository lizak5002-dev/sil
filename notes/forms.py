from django import forms
from .models import Note
from django_ckeditor_5.widgets import CKEditor5Widget

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'context': CKEditor5Widget(attrs={"class": "django_ckeditor_5, 'placeholder': 'Введите текст'"}, config_name="default")
        }
        labels = {
            'title': 'Название заметки',
            'context': 'Текст заметки'
        }
 