from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.contrib import messages

def post_list(request):
    posts = Post.objects.all().filter(status="published").select_related("author", "category")
    context = {
        "posts": posts,
        "title": "Блог"
    }
    return render(request, "blog/post_list.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)


@login_required
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = "pending"
            post.save()
            messages.success(request, "Пост успешно добавлен и отправлен на модерацию! Он будет опубликован после проверки.")
            return redirect(reverse("blog:post_list"))
    else:
        form = PostForm()
        context = {
            "form":form,
            "title": "Создание поста"
        }
        return render(request, "blog/post_add.html", context)
    
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Пост успешно удалён!")
        return redirect(reverse("blog:post_list"))
    context = {
        'post': post,
        'title':'Удаление поста'
    }
    return render(request, "blog/post_delete.html", context)


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Пост успешно обновлен!")
            return redirect(reverse("blog:post_list"))
    else:
        form = PostForm(instance=post)
    context = {'form':form, 'title':'Редактирование поста'}
    return render(request, 'blog/post_update.html', context)
