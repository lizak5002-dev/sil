from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from .moderation import ModerationBlog

CHOICE_STATUS = (
        ("draft", "Черновик"),
        ("pending", "На модерации"),
        ("published", "Опубликован"),
        ('rejected', 'Отклонён'),
    )

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Категория")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Post(models.Model):

    title = models.CharField(max_length=100, verbose_name="Название")
    lead = models.CharField(max_length=200, default='', blank=True, verbose_name="Краткое описание")
    content = CKEditor5Field(verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    image = models.ImageField(upload_to='posts/images/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение')
    status = models.CharField(max_length=15, choices=CHOICE_STATUS, verbose_name="Статус", default="draft")
    moderation_reason = models.TextField(blank=True, verbose_name="Причина модерации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["created_at"]

    def auto_moderate(self):
        '''Автоматическая генерация поста'''

        moderator = ModerationBlog()
        is_clean, bad_words = moderator.check_post(self.title, self.content)
        if is_clean:
            self.status = "published"
            self.moderation_reason = "Автоматически одобрено"
        else:
            self.status = "rejected"
            bad_words_str = ", ".join(bad_words)
            self.moderation_reason = f"Найдены запрещенные слова: {bad_words_str}"

        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Автор")
    content = models.TextField(max_length=1000, verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    status = models.CharField(max_length=15, choices=CHOICE_STATUS, verbose_name="Статус", default="pending")
    moderation_reason = models.TextField(blank=True, verbose_name="Причина модерации")

    def __str__(self):
        return f"Комментарий от {self.author} к '{self.post.title}'"
    
    def moderate_comment(self):
        comment_moderator = ModerationBlog()
        is_clean, bad_words = comment_moderator.check_text(self.content)
        if is_clean:
            self.status = "published"
            self.moderation_reason = "Автоматически одобрено"
            return True
        else:
            self.status = "rejected"
            bad_words_str = ", ".join(bad_words)
            self.moderation_reason = f"Найдены запрещенные слова: {bad_words_str}"
            return False

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
