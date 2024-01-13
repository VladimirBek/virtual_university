from rest_framework.fields import SerializerMethodField

from main.models import Course, Lesson, Payment
from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class UserDetailSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    def get_payments(self, user):
        return [(el.date_pay, el.amount) for el in Payment.objects.filter(user=user)]

    class Meta:
        model = User
        fields = ("email", "phone_number", "city", "payments")
