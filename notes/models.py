from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    content = CKEditor5Field(max_length=10_000, verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    

