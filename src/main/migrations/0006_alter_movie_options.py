# Generated by Django 3.2 on 2021-06-09 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210520_1102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-id']},
        ),
    ]