# Generated by Django 5.0 on 2024-01-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_lesson_options_remove_lesson_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_link',
            field=models.URLField(blank=True, max_length=30, null=True, verbose_name='ссылка на видео'),
        ),
    ]
