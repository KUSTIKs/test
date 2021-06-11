# Generated by Django 3.2 on 2021-05-02 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('icon_name', models.CharField(default='film-frames', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
                ('year', models.PositiveSmallIntegerField()),
                ('poster', models.ImageField(null=True, upload_to='movies/poster')),
                ('country', models.CharField(max_length=100)),
                ('short', models.ImageField(blank='true', null=True, upload_to='movies/shortcut')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('hide', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='profile/image/avatar-1.png', upload_to='profiles/image')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='stars/photo/')),
            ],
        ),
        migrations.CreateModel(
            name='SavedMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ManyToManyField(related_name='savedmovie_movie', to='main.Movie', verbose_name='movie')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='movie_actor', to='main.Star'),
        ),
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category'),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(related_name='movie_director', to='main.Star'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='main.Genre', verbose_name='genres'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.movie')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile', verbose_name='user')),
            ],
            options={
                'ordering': ('-created_date', 'profile__user__username'),
            },
        ),
    ]
