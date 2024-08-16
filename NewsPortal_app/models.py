from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def upgrade_rating(self):
        total_rating = 0
        for elem_post in Post.objects.filter(author_id=self.pk):
            total_rating += elem_post.post_rating * 3
            for elem_comment in Comment.objects.filter(post_id=elem_post):
                total_rating += elem_comment.rating_comment

        for elem_user_comment in Comment.objects.filter(user_id=self.author_user):
            total_rating += elem_user_comment.rating_comment
        self.author_rating = total_rating
        self.save()

    def __str__(self):
        return self.author_user.username


class Category(models.Model):

    CATEGORY_LIST = [
        ('PO', "Политика"),
        ('SP', "Спорт"),
        ('EC', "Экономика"),
        ('SC', "Наука"),
        ('TE', "Технологии"),
        ('FI', "Фантастика"),
        ('MY', "Мистика"),
        ('FA', "Фэнтези"),
        ('DE', "Детектив"),
        ('HI', "История"),
    ]

    category_name = models.CharField(max_length=2, unique=True, choices=CATEGORY_LIST, default='PO')

    def __str__(self):
        for i in range(len(self.CATEGORY_LIST)):
            if self.CATEGORY_LIST[i][0] == self.category_name:
                return self.CATEGORY_LIST[i][1]


class Post(models.Model):

    TYPE_POST = [
        ('N', "Новости"),
        ('A', "Статья")
    ]

    type_post = models.CharField(max_length=1, choices=TYPE_POST, default='A')
    time_create = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_content = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_content[:124] + '...'

    def __str__(self):
        return self.post_title[:20]

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"post-{self.pk}")


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
