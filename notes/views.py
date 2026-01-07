from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def show_notes(request):
    notes = Note.objects.all().order_by('-created_at')
    context = {
        'notes': notes,
    }
    return render(request, 'notes/notes_list.html', context)

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, 'Заметка успешно добавлена!')
            return redirect('show_notes')
    else:
        note = NoteForm()
    return render(request, 'notes/notes_form.html', {'form': note, 'title': 'Добавить заметку'})

def edit_note():
    pass

def delete_note():
    pass