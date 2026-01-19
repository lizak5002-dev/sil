from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.show_notes, name='show_notes'),
    path('create/', views.create_note, name='create_note'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('delete/<int:id>/', views.delete_note, name='delete_note'),
]

#myay