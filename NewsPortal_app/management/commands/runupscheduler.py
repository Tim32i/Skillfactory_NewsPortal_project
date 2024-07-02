import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from NewsPortal_app.models import Post, Category, Subscriber

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories_id = set(posts.values_list('categories', flat=True).values_list('post_category__pk', flat=True))
    subscribers = []
    for category_id in categories_id:
        subscribers += Category.objects.get(pk=category_id).subscribers.all()
    subscribers = set(subscribers)                                               # убираем дубляж

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

    for subscriber in subscribers:
        print('subsciber:', subscriber)
        print(subscriber.user.email)
        msg = EmailMultiAlternatives(
            subject=msg_subject,
            body=msg_body,
            from_email=msg_from_email,
            to=[subscriber.user.email,]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
        This job deletes APScheduler job execution entries older than `max_age`
        from the database.
        It helps to prevent the database from filling up with old historical
        records that are no longer useful.

        :param max_age: The maximum length of time to retain historical
                        job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'. ")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shutdown successfully!")
