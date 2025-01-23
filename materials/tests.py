from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from materials.serializers import LessonSerializer
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="password")
        self.moderator = User.objects.create(
            email="moderator@test.com", password="password"
        )
        moderators = self.moderator.groups.create(name="moders")
        self.moderator.groups.add(moderators)
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            owner=self.user,
        )

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = f"http://localhost:8000/materials/lesson/{self.lesson.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.get(id=self.lesson.id)
        serializer = LessonSerializer(lesson)
        self.assertEqual(response.data, serializer.data)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "owner": self.user.id,
        }
        if not User.objects.filter(id=1).exists():
            self.fail("User with ID=1 does not exist in the database")
        response = self.client.post(
            "http://localhost:8000/materials/lesson/create/", data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        url = "http://localhost:8000/materials/lesson/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = f"http://127.0.0.1:8000/materials/lesson/update/{self.lesson.id}/"
        data = {
            "name": "Updated Lesson",
            "description": "Updated Lesson Description",
            "course": self.course.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.get(id=self.lesson.id)
        self.assertEqual(lesson.name, data["name"])
        self.assertEqual(lesson.description, data["description"])

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = f"http://127.0.0.1:8000/materials/lesson/delete/{self.lesson.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)

    def test_subscribes(self):
        self.client.force_authenticate(user=self.user)
        url = "http://127.0.0.1:8000/materials/subscribe/"
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
