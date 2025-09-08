from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscriber
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    model=Post


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Subscriber)



