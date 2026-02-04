from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    content = CKEditor5Field(max_length=10_000, verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено в")
    deleted_at = models.DateTimeField(null=True, blank=True)  
    pinned_at = models.DateTimeField(null=True, blank=True, verbose_name="Закреплено в")
    is_deleted = models.BooleanField(default=False)  
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")  

    def __str__(self):
        return self.title
    
    def soft_delete(self):
        """Мягкое удаление заметки"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Восстановление заметки из корзины"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def toggle_pin(self):
        """Переключение состояния закрепления"""
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            Note.objects.filter(id=self.id).update(
                is_pinned=True,
                pinned_at=timezone.now()
            )
        else:
            Note.objects.filter(id=self.id).update(
                is_pinned=False,
                pinned_at=None
            )
        
        self.refresh_from_db()
        return self.is_pinned

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ['-is_pinned', '-updated_at']

    

