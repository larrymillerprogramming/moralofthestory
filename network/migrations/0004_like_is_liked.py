# Generated by Django 3.1.6 on 2021-02-21 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210219_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='is_liked',
            field=models.BooleanField(default=True),
        ),
    ]
