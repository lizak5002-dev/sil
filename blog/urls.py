from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post_add/', views.post_add, name="post_add"),
    path('post_delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('post_update/<int:post_id>/', views.post_update, name='post_update'),
]