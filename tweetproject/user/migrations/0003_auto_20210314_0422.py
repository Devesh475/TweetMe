# Generated by Django 3.0.2 on 2021-03-13 22:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_userform_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userform',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
