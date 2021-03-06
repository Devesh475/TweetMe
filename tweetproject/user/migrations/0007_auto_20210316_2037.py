# Generated by Django 3.0.2 on 2021-03-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210314_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='userform',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userform',
            name='contactNumber',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userform',
            name='firstName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userform',
            name='gender',
            field=models.CharField(choices=[('Male', 'M'), ('Female', 'F'), ('Other', 'O')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userform',
            name='lastName',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
