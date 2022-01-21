from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Task

# Create your tests here.


class TstTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username="dev1")
        self.user1.set_password("Test123")
        self.user2 = User.objects.create(username="dev2")
        self.user1.set_password("Test123")
        self.url = "/api/v1/tasks/"

    def test_get_request(self):
        task1 = Task.objects.create(user=self.user1, name="task1", deadline=timezone.now())
        task2 = Task.objects.create(user=self.user2, name="task2", deadline=timezone.now())

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]["user"]["username"], "dev1")
        self.assertEqual(response.json()[0]["id"], task1.id)
        self.client.logout()

    def test_task_create(self):
        self.client.force_authenticate(user=self.user1)
        data = {
                "name": "Read Book",
                "deadline": "2022-01-24T11:00"
            }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]["status"], "in_progress")

        self.client.logout()

    def test_task_update(self):
        self.client.force_authenticate(user=self.user1)
        data = {
                "name": "Cook Meat",
                "deadline": "2022-01-24T11:00"
            }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]["status"], "in_progress")

        update_data = {
            "status": "working_now",
        }

        update_response = self.client.patch(f"{self.url}1/", update_data, format="json")
        self.assertEqual(update_response.json()["status"], "working_now")
        self.assertEqual(update_response.status_code, 200)

        self.client.logout()

    def test_task_delete(self):
        self.client.force_authenticate(user=self.user1)
        data = {
                "name": "Cook Meat",
                "deadline": "2022-01-24T11:00"
            }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(f"{self.url}1/", format="json")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_prevent_task_delete_of_other_user(self):
        task1 = Task.objects.create(user=self.user1, name="task1", deadline=timezone.now())
        task2 = Task.objects.create(user=self.user2, name="task2", deadline=timezone.now())

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(f"{self.url}{task2.id}/", format="json")
        self.assertEqual(response.status_code, 404)
