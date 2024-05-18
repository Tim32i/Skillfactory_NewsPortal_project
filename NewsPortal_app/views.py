from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, PostCategory

class PostListView(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

