from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sessions.models import Session
from django.db.models import Exists, OuterRef
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Post, PostCategory, Category, Subscriber
from .filters import NewsFilter
from .forms import PostForm
from .tasks import notify_about_new_post


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_categories_id = PostCategory.objects.filter(post=self.object).values('category')
        context['categories'] = Category.objects.filter(id__in=post_categories_id)
        return context


class NewsCreateView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    permission_required = 'NewsPortal_app.add_post'
    raise_exception = True
    form_class = PostForm
    template_name = 'news_create.html'
    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'N'
        post_new = Post.objects.create(type_post=type_post,
                                       post_title=post_title,
                                       post_content=post_content,
                                       author=author
                                       )
        post_new.save()

        categories_list_id = Category.objects.filter(pk__in=categories).values('id')
        for category_id in categories_list_id:
            post_new.post_category.add(category_id['id'])                   # срабатывает m2m_changed
        post_new.save()
        notify_about_new_post.apply_async([post_new.pk], countdown=1)


        if form.is_valid():
            return HttpResponseRedirect(f'/news/search/{post_new.pk}')

class ArticleCreateView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    permission_required = 'NewsPortal_app.add_post'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'A'
        post_new = Post.objects.create(type_post=type_post,
                                   post_title=post_title,
                                   post_content=post_content,
                                   author=author
                                   )
        post_new.save()

        categories_list_id = Category.objects.filter(pk__in=categories).values('id')
        for category_id in categories_list_id:
            post_new.post_category.add(category_id['id'])                     # срабатывает m2m_changed
        post_new.save()
        notify_about_new_post.apply_async([post_new.pk], countdown=1)

        if form.is_valid():
            return HttpResponseRedirect(f'/news/{post_new.pk}')


class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'NewsPortal_app.change_post'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'N'
        post_updated = self.object
        post_updated.type_post=type_post
        post_updated.post_title=post_title
        post_updated.post_content=post_content
        post_updated.author=author
        post_updated.save()

        category_list = Category.objects.filter(pk__in=categories)

        PostCategory.objects.filter(post=post_updated).delete()   # удаляем все предыдущие категории

        # в цикле добавляем новые категории, при этом m2m_changed не срабатывает, т.к. поле manytomany
        # (post_updated.post_category) не затрагивается.

        for category in category_list:
            post_category = PostCategory.objects.create(post=post_updated, category=category)
            post_category.save()

        if form.is_valid():
            return HttpResponseRedirect(f'/news/search/{post_updated.pk}')


class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'NewsPortal_app.change_post'
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'A'
        post_updated = self.object
        post_updated.type_post = type_post
        post_updated.post_title = post_title
        post_updated.post_content = post_content
        post_updated.author = author
        post_updated.save()

        category_list = Category.objects.filter(pk__in=categories)

        PostCategory.objects.filter(post=post_updated).delete()           # удаляем все предыдущие категории

        # в цикле добавляем новые категории, при этом m2m_changed не срабатывает, т.к. поле manytomany
        # (post_updated.post_category) не затрагивается.

        for category in category_list:
            post_category = PostCategory.objects.create(post=post_updated, category=category)
            post_category.save()

        if form.is_valid():
            return HttpResponseRedirect(f'/news/{post_updated.pk}')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'NewsPortal_app.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


@login_required
@csrf_protect
def subsciptions(request):
    if request.method =='POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id = category_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(user=request.user, category=OuterRef('pk'))
        )
    ).order_by('category_name')

    return render(request,
                  'subscriptions.html',
                  {'categories': categories_with_subscriptions})



