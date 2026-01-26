from django import forms
from .models import Post, Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "image", "title", "lead", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите заголовок поста"}), 
            "lead": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите краткое описание"}), 
            "content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="default"), 
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].empty_label = "Выберите категорию"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите ваш комментарий...'
            })
        }
