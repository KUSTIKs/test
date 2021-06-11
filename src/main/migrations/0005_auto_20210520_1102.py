# Generated by Django 3.2 on 2021-05-20 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_movie_trailer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='trailer',
        ),
        migrations.AddField(
            model_name='movie',
            name='video_id',
            field=models.SlugField(default='ykw5NFywYuw', max_length=200),
        ),
    ]
