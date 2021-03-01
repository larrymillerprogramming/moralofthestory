# Generated by Django 3.1.6 on 2021-02-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_like_is_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='is_liked',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='like',
            name='postId',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
