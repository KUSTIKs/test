# Generated by Django 3.2 on 2021-05-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='/profile/image/avatar-1.png', upload_to='profiles/image'),
        ),
    ]
