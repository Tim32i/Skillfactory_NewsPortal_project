# Generated by Django 4.2.13 on 2024-05-17 06:44

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
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_rating', models.IntegerField(default=0)),
                ('author_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(choices=[('PO', 'Политика'), ('SP', 'Спорт'), ('EC', 'Экономика'), ('SC', 'Наука'), ('TE', 'Технологии'), ('FI', 'Фантастика'), ('MY', 'Мистика'), ('FA', 'Фэнтези'), ('DE', 'Детектив'), ('HI', 'История')], default='PO', max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_post', models.CharField(choices=[('N', 'Новости'), ('A', 'Статья')], default='A', max_length=1)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('post_title', models.CharField(max_length=255)),
                ('post_content', models.TextField()),
                ('post_rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal_app.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal_app.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal_app.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(through='NewsPortal_app.PostCategory', to='NewsPortal_app.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time_comment', models.DateTimeField(auto_now_add=True)),
                ('rating_comment', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal_app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
