from rest_framework import status
from rest_framework.test import APITestCase

from models import Course, Subscription
from models import Lesson

from users.models import User


class LessonsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test-sky-org@gmail.com",
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            owner=self.user,
            name="Тестовый курс",
            description="Описание тестового курса",
            url="https://youtube.com",
        )

    def test_create_lesson(self):
        data = {
            "owner": 1,
            "name": "name",
            "description": "description",
            "url": "https://youtube.com",
            "course": 1,
        }

        response = self.client.post(
            "/api/v1/lessons/create/",
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().name, "name")

    def test_delete_lesson(self):
        data = {
            "owner": self.user,
            "name": "name",
            "description": "description",
            "url": "https://youtube.com",
        }

        lesson = Lesson.objects.create(**data)
        lesson.course.add(self.course)

        response = self.client.delete(f"/api/v1/lessons/delete/{lesson.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(Lesson.objects.all().count(), 0)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())

    def test_get_lesson(self):
        data = {
            "owner": self.user,
            "name": "name",
            "description": "description",
            "url": "https://youtube.com",
        }

        lesson = Lesson.objects.create(**data)
        lesson.course.add(self.course)

        response = self.client.get(
            f"/api/v1/lessons/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(Lesson.objects.get().name, "name")

    def test_update_lesson(self):
        data = {
            "owner": self.user,
            "name": "name",
            "description": "description",
            "url": "https://youtube.com",
        }

        lesson = Lesson.objects.create(**data)
        lesson.course.add(self.course)

        data_for_update = {
            "owner": self.user.id,
            "name": "name_update",
            "description": "description",
            "url": "https://youtube.com",
            "course": self.course.id,
        }

        response = self.client.put(
            f"/api/v1/lessons/update/{lesson.id}/",
            data_for_update,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(Lesson.objects.get().name, "name_update")


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test-sky-org@gmail.com'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            owner=self.user,
            name='Тестовый курс',
            description='Описание тестового курса',
            url='https://youtube.com',
        )


    def test_subscription_create(self):
        data = {
            'course': self.course.id,
            'is_active': True

        }

        response = self.client.post(f'/api/v1/subscriptions/create/', data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Subscription.objects.all().count(), 1)
        self.assertEquals(Subscription.objects.get(course=self.course.id).user, self.user)
        self.assertTrue(Subscription.objects.get(course=self.course.id).is_active, True)

    def test_subscription_delete(self):
        data = {
            'course': self.course,
            'is_active': True,
            "user": self.user

        }
        sub = Subscription.objects.create(**data)

        response = self.client.delete(f'/api/v1/subscriptions/delete/{sub.id}/')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Subscription.objects.all().count(), 0)