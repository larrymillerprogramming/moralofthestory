# Generated by Django 3.1.6 on 2021-02-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210221_0404'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='is_liked',
            field=models.BooleanField(default=True),
        ),
    ]
