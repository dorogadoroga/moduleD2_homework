import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from  django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category


logger = logging.getLogger(__name__)

def my_job():
    date_today = datetime.utcnow()
    date = date_today - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(category=category, date__gt=date)
        if posts:
            posts_texts = []
            for post in posts:
                posts_texts.append(post.title)
                posts_texts.append(post.text)
            posts_texts = '\n'.join(posts_texts)
            print(posts_texts)
            for user in category.subscribers.all():
                html_content = render_to_string('mail/posts_for_week.html', {'posts': posts, 'user': user})
                msg = EmailMultiAlternatives(
                    subject=f'Новости за неделю',
                    body=posts_texts,
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second='*/10'),
            # (day_of_week="sun", hour="00", minute="00")
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
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")