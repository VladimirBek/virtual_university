# Generated by Django 5.0 on 2023-12-24 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_course_owner_lesson_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='url',
            field=models.URLField(blank=True, default='youtube.com', max_length=30, null=True, verbose_name='ссылка на курс'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='подписка')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
