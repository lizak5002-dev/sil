from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def post_list(request):
    posts = Post.objects.all().filter(status="published").select_related("author", "category")
    search_query = request.GET.get("q")
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    category_search = request.GET.get("category")
    if category_search:
        posts = posts.filter(category__id=category_search)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)
    context = {
        "posts": page_posts,
        "title": "Блог"
    }
    return render(request, "blog/post_list.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    comments = Comment.objects.filter(post=post, status = "published").order_by("created_at")
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Нужно авторизоваться, чтобы оставлять комментарии!")
            return redirect(reverse("users:login"))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if comment.moderate_comment():
                comment.save()
                messages.success(request, "Комментарий успшно опубликован!")
            else:
                comment.save()
                messages.warning(request, "Комментарий нарушает правила!")
            return redirect(reverse("blog:post_detail", args=[post_id ]))
    else:
        comment_form = CommentForm()
    post.views += 1
    post.save(update_fields=["views"])
    context = {
        "post":post,
        "title": post.title,
        "comments": comments,  
        "comment_form": comment_form
    }
    return render(request, "blog/post_detail.html", context)

@login_required
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        save_action = request.POST.get("action", "publish")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if save_action == "draft":
                post.status = "draft"
                post.save()
                messages.success(request, "Пост успешно сохранён как черновик!")
                return redirect(reverse("blog:post_list"))
            elif save_action == "publish":
                post.status = "pending"
                post.save()
                post.auto_moderate()
                if post.status == "published":
                    messages.success(request, "Пост успешно опубликован!")
                elif post.status == "rejected":
                    messages.warning(request, f"Пост отклонен, так как нарушает правила публикации!")
                else:
                    messages.success(request, "Пост отправлен на модерацию! Он будет опубликован после проверки.")
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
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        messages.error(request, "Вы не можете удалить чужой пост!")
        return redirect("blog:post_list")
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
    save_action = request.POST.get("action", "published")
    if request.user != post.author:
        messages.error(request, "Вы не можете изменять чужой пост!")
        return redirect("blog:post_list")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if save_action == "draft":
                post.status = "draft"
                post.save()
                messages.success(request, "Пост успешно сохранён как черновик!")
                return redirect(reverse("blog:post_list"))
            elif save_action == "publish":
                post.status = "pending"
                post.save()
                post.auto_moderate()
                if post.status == "published":
                    messages.success(request, "Пост успешно Обновлён!")
                elif post.status == "rejected":
                    messages.warning(request, f"Пост отклонен, так как нарушает правила публикации!")
                else:
                    messages.success(request, "Пост отправлен на модерацию! Он будет опубликован после проверки.")
                return redirect(reverse("blog:post_list"))
    else:
        form = PostForm(instance=post)
    context = {'form':form, 'title':'Редактирование поста'}
    return render(request, 'blog/post_update.html', context)
