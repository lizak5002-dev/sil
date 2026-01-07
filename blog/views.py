from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.all().filter(status="published").select_related("author", "category")
    context = {
        "posts": posts,
        "title": "Блог"
    }
    return render(request, "blog/post_list.html", context)

def add_post(request):
    form = PostForm()
    context = {
        "form":form,
        "title": "Создание поста"
    }
    return render(request, "blog/add_post.html", context)