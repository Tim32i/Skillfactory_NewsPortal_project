from django import forms
from .models import Post, Category

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_content',
            'author',
            ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_content',
            'author',
            ]