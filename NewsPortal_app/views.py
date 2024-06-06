from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostCategory
from .filters import NewsFilter
from .forms import NewsForm, ArticleForm

class PostListView(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsListView(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        queryset = Post.objects.filter(type_post__exact='N')
        self.filterset = NewsFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreateView(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'N'
        return super().form_valid(form)


class ArticleCreateView(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'A'
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_update.html'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'N'
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'A'
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

