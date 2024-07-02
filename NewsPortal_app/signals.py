from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .models import PostCategory, Post
from .settings import *

def send_notifications(preview, pk, title, subscribers, type_post):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/news/{pk}',
            'type_post': type_post,
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email= DEFAULT_FROM_EMAIL,
            to=[subscriber, ],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
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

        send_notifications(instance.preview(), instance.pk, instance.post_title,
                           new_post_subscribers_email, instance.type_post)
