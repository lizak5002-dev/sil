from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import Note
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def show_notes(request):
    notes = Note.objects.all().order_by('-updated_at').filter(is_deleted=False)
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
            messages.success(request, 'Заметка добавлена')
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
                messages.success(request, 'Заметка обновлена')
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
        messages.success(request, 'Заметка удалена')
        return redirect('notes:show_notes')
    except Note.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")
    

@login_required
def notes_basket(request):
    deleted_notes = Note.objects.all().filter(is_deleted=True, author=request.user)
    context = {
        'notes': deleted_notes,
    }
    return render(request, 'notes/notes_basket.html', context)

@login_required
def delete_note_soft(request, id):
    try:
        note = Note.objects.get(id=id)

        if note.author != request.user:
            raise PermissionDenied
    
        note.soft_delete()
        messages.success(request, 'Заметка перемещена в корзину')
        return redirect('notes:show_notes')
    except Note.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")
    
@login_required
def restore_note(request, id):
    try:
        note = Note.objects.get(id=id)

        if note.author != request.user:
            raise PermissionDenied
    
        if note.is_deleted:
            note.restore()

        messages.success(request, 'Заметка восстановлена')
        return redirect('notes:show_notes')
    except Note.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")
    
@login_required
def toggle_pin(request, id):
    """Переключение состояния закрепления заметки"""
    note = get_object_or_404(Note, id=id, author=request.user)
    is_pinned = note.toggle_pin()
    
    if is_pinned:
        messages.success(request, 'Заметка закреплена')
    else:
        messages.success(request, 'Заметка откреплена')
    
    return redirect(request.META.get('HTTP_REFERER', 'show_notes'))