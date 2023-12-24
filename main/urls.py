from django.urls import path
from rest_framework import routers

from main.apps import MainConfig
from main.models import Lesson
from main.views import CourseViewSet, LessonListAPI, LessonCreateAPI, LessonRetrieveAPI, LessonUpdateAPI, \
    LessonDestroyAPI, PaymentListView, PaymentCreateView

app_name = MainConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = [
                  path('lessons/', LessonListAPI.as_view(), name='lesson-list'),
                  path('lessons/create/', LessonCreateAPI.as_view(), name='lesson-create'),
                  path('lessons/<int:pk>/', LessonRetrieveAPI.as_view(), name='lesson-get'),
                  path('lessons/update/<int:pk>/', LessonUpdateAPI.as_view(), name='lesson-update'),
                  path('lessons/delete/<int:pk>/', LessonDestroyAPI.as_view(), name='lesson-delete'),
                  path('payments/', PaymentListView.as_view(), name='payment-list'),
                  path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
                  path('subscriptions/create/', SubscriptionCreate.as_view(), name='create_view'),
                  path('subscriptions/', SubscriptionList.as_view(), name='list_view'),
                  path('subscriptions/delete/<int:pk>/', SubscriptionDelete.as_view(), name='delete_view'),
              ] + router.urls
