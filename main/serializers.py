from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from main.models import Course, Lesson, Payment, Subscription
from main.validators import UrlValidate
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidate(value="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UrlValidate(value="video_link")]

    def get_count_lessons(self, course):
        count = int(course.lesson_set.count())
        return count

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()

    def get_user(self, subscription):
        return User.objects.get(subscription=subscription).email

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

