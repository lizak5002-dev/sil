from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.show_notes, name='show_notes'),
    path('create/', views.create_note, name='create_note'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('delete/<int:id>/', views.delete_note, name='delete_note'),
    path('basket/', views.notes_basket, name='notes_basket'),
    path('soft_delete/<int:id>/', views.delete_note_soft, name='delete_note_soft'),
    path('restore/<int:id>/', views.restore_note, name='restore_note'),
]

#myay