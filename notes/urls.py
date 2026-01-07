from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('show/', views.show_notes, name='show_notes'),
    path('create/', views.create_note, name='create_note'),
    path('edit/', views.edit_note, name='edit_note'),
    path('delete/', views.delete_note, name='delete_note'),
]

#myay