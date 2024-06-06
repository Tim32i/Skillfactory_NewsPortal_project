from django.urls import path
from .views import PostListView, NewsListView, PostDetailView, NewsCreateView, ArticleCreateView, \
    NewsUpdateView, ArticleUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('search/', NewsListView.as_view()),
    path('news/create/', NewsCreateView.as_view(), name='create_news'),
    path('articles/create', ArticleCreateView.as_view(), name='create_article'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='update_news'),
    path('articles/<int:pk>/edit', ArticleUpdateView.as_view(), name='update_article'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('articles/<int:pk>/delete', PostDeleteView.as_view(), name='delete_post'),
    path('<pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/<pk>', PostDetailView.as_view(), name='post_detail'),

]