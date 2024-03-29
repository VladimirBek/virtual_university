from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    owner = models.ForeignKey('users.User', verbose_name='владелец курса', on_delete=models.CASCADE, **NULLABLE)
    preview = models.ImageField(upload_to='course', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    video_link = models.ManyToManyField('Lesson', related_name='lesson_set')
    url = models.URLField(max_length=30, default="youtube.com", verbose_name='ссылка на курс', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    owner = models.ForeignKey('users.User', verbose_name='владелец урока', on_delete=models.CASCADE, **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course', verbose_name='превью', **NULLABLE)
    video_link = models.URLField(max_length=30, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ManyToManyField("Course", verbose_name='курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
    payment_intent_id = models.CharField(max_length=50, **NULLABLE)

    def __str__(self):
        return f"{self.user.email} - {self.payment_date} - {self.user}"


class Subscription(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='подписка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.user} | {self.course.name}'