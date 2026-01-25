from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('post_add/', views.post_add, name="post_add"),
]