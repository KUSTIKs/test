# Generated by Django 3.2 on 2021-05-19 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210502_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer',
            field=models.URLField(default='https://youtu.be/0kMqRhJ_A0c'),
        ),
    ]
