from celery import shared_task
from .models import Post, PostCategory, Category
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import *
def send_notifications(preview, pk, title, subscribers, type_post):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
            'type_post': type_post,
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber, ],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def notify_about_new_post(oid):
    instance = Post.objects.get(pk=oid)
    new_post_categories = instance.post_category.all()
    new_post_subscribers_id = []
    for new_post_category in new_post_categories:
        new_post_subscribers_id += new_post_category.subscribers.all().values('user')
    new_post_subscribers_id = [s['user'] for s in new_post_subscribers_id]
    new_post_subscribers_id = set(new_post_subscribers_id)                 # исключение дубляжа подписчиков
    new_post_subscribers = [User.objects.get(id=sub_id)
                            for sub_id in new_post_subscribers_id]

    new_post_subscribers_email = [user.email for user in new_post_subscribers]

#       subscribers = [s.email for s in subscribers]

    send_notifications(instance.preview(), oid, instance.post_title,
                       new_post_subscribers_email, instance.type_post)


@shared_task
def weekly_new_post_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories_id = set(posts.values_list('categories', flat=True).values_list('post_category__pk', flat=True))
    subscribers = []
    for category_id in categories_id:
       subscribers += Category.objects.get(pk=category_id).subscribers.all()

    # рассылка писем

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg_subject = 'Посты за неделю'
    msg_body = ''
    msg_from_email = settings.DEFAULT_FROM_EMAIL

    subscribers_emails = [subscriber.user.email for subscriber in subscribers]   # список email
    subscribers_emails = set(subscribers_emails)                                 # убираем дубли


    for subscriber_email in subscribers_emails:

        msg = EmailMultiAlternatives(
            subject=msg_subject,
            body=msg_body,
            from_email=msg_from_email,
            to=[subscriber_email,]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

