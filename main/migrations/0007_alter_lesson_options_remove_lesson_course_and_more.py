# Generated by Django 5.0 on 2024-01-04 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_course_url_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='course',
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ManyToManyField(to='main.course', verbose_name='курс'),
        ),
    ]
