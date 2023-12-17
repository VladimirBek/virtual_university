from django.urls import path
from rest_framework import routers

from main.apps import MainConfig
from main.models import Lesson
from main.views import CourseViewSet, LessonListAPI, LessonCreateAPI, LessonRetrieveAPI, LessonUpdateAPI, \
    LessonDestroyAPI

app_name = MainConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = [
    path('lessons/', LessonListAPI.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPI.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPI.as_view(), name='lesson-get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPI.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPI.as_view(), name='lesson-delete')
] + router.urls
