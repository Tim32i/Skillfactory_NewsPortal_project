from django.forms.widgets import SelectMultiple
from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    post_category = forms.ModelMultipleChoiceField(label='Категории', queryset=Category.objects.all(),
                                                   widget=SelectMultiple(attrs={'size': 10}))

    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_content',
            'author',
            'post_category',
            ]
