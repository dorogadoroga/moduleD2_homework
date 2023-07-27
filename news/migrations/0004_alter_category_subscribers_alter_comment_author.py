# Generated by Django 4.2.2 on 2023-07-27 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, through='news.UserCategory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
