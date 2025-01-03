from rest_framework.test import APITestCase
from users.models import Subscription, User
from materials.models import Course, Lesson
from django.urls import reverse
from rest_framework import status


class SubscriptionTests(APITestCase):

    def setUp(self):
        email = "test@mail.ru"
        password = "test12345"
        self.user = User.objects.create_user(email=email, password=password, username='test')
        self.course = Course.objects.create(name="Python", description="sbj")
        self.data = {"course_id": self.course.pk}
        token = self.client.post(reverse("users:login"), {"email": email, "password": password}).json()["access"]
        self.headers = {"Authorization": f"Bearer {token}"}

    def test_subscribe(self):
        url = reverse("users:subscribe")
        response = self.client.post(url, self.data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Subscription.objects.get(user=self.user, course=self.course)

    def test_unsubscribe(self):
        url = reverse("users:subscribe")
        response = self.client.post(url, self.data, headers=self.headers)
        url = reverse("users:unsubscribe")
        response = self.client.post(url, self.data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(Subscription.objects.filter(user=self.user, course=self.course)) == 0

    def tearDown(self):
        pass


class LessonsTests(APITestCase):

    def setUp(self):
        email = "test@mail.ru"
        password = "test12345"
        self.user = User.objects.create_user(email=email, password=password, username='test')
        self.course = Course.objects.create(name="Python", description="sbj")
        token = self.client.post(reverse("users:login"), {"email": email, "password": password}).json()["access"]
        self.headers = {"Authorization": f"Bearer {token}"}

    def test_create_lesson(self):
        data = {
            "name": "strings in python",
            "description": "about strings in python",
            "video_url": "https://www.youtube.com/watch?v=Ctqi5Y4X-jA",
            "course": self.course.pk
        }
        url = "/materials/lesson/"
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Lesson.objects.get(name=f"{data["name"]}")

    def test_retrieve_lesson(self):
        data = {
            "name": "strings in python",
            "description": "about strings in python",
            "video_url": "https://www.youtube.com/watch?v=Ctqi5Y4X-jA",
            "course": self.course.pk
        }
        url = "/materials/lesson/"
        response = self.client.post(url, data, headers=self.headers)
        lesson_id = Lesson.objects.all()[0].pk
        response = self.client.get(f"/materials/lesson/{lesson_id}", headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_update_lesson(self):
        data = {
            "name": "strings in python",
            "description": "about strings in python",
            "video_url": "https://www.youtube.com/watch?v=Ctqi5Y4X-jA",
            "course": self.course.pk
        }
        url = "/materials/lesson/"
        response = self.client.post(url, data, headers=self.headers)
        lesson = Lesson.objects.get(name=f"{data["name"]}")

        data["name"] = "new_name"
        id = lesson.pk
        response = self.client.patch(f"{url}{id}/", data, headers=self.headers)
        Lesson.objects.get(name="new_name")

    def test_delete_lesson(self):
        data = {
            "name": "strings in python",
            "description": "about strings in python",
            "video_url": "https://www.youtube.com/watch?v=Ctqi5Y4X-jA",
            "course": self.course.pk
        }
        url = "/materials/lesson/"
        response = self.client.post(url, data, headers=self.headers)
        lesson = Lesson.objects.get(name=f"{data["name"]}")
        id = lesson.pk
        response = self.client.delete(f"{url}{id}/", headers=self.headers)

    def tearDown(self):
        pass
