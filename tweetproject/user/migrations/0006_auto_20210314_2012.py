# Generated by Django 3.0.2 on 2021-03-14 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userform_followed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userform',
            old_name='followed',
            new_name='following',
        ),
    ]
