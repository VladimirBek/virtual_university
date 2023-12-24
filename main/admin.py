from django.contrib import admin

from .models import Payment, Course, Lesson, Subscription

admin.site.register(Payment)
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Subscription)

