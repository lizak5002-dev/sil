from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'context']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'context': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите текст'})
        }
        labels = {
            'title': 'Название заметки',
            'context': 'Текст заметки'
        }
 