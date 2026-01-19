from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def show_notes(request):
    notes = Note.objects.all().order_by('-created_at')
    context = {
        'notes': notes,
    }
    return render(request, 'notes/notes_list.html', context)

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, 'Заметка успешно добавлена!')
            return redirect('notes:show_notes')
    else:
        form = NoteForm()
    return render(request, 'notes/notes_form.html', {'form': form, 'title': 'Добавить заметку'})

@login_required
def edit_note(request, id):
    try:
        note = Note.objects.get(id=id)

        if note.author != request.user:
            raise PermissionDenied
    
        if request.method == "POST":
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                note = form.save(commit=False)
                note.author = request.user
                note.save()
                messages.success(request, 'Заметка успешно обновлена!')
                return redirect('notes:show_notes')
        else:
            form = NoteForm(instance=note)
        return render(request, 'notes/notes_form.html', {'form': form, 'title': 'Изменить заметку'})
    except Note.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")

@login_required
def delete_note(request, id):
    try:
        note = Note.objects.get(id=id)

        if note.author != request.user:
            raise PermissionDenied
    
        note.delete()
        return redirect('notes:show_notes')
    except Note.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")
