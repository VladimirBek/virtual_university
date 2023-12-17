from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to='course', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course', verbose_name='превью', **NULLABLE)
    video_link = models.CharField(max_length=150, verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


