import json
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from jwt_auth.models import User
from . import models


class APITestCase(TestCase):
    admin_data = {
        'username': 'admin',
        'email': 'admin@gmail.com',
        'password': 'rootconfig'
    }

    admin2_data = {
        'username': 'admin2',
        'email': 'adminTwo@gmail.com',
        'password': 'twoconfig'
    }

    user_data = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'testuserpwd'
    }

    @staticmethod
    def _get_data(rsp) -> dict:
        data = json.loads(rsp.content.decode())
        return data

    @staticmethod
    def _headers(token) -> dict:
        return {'Authorization': f'Bearer {token}'}

    def _get_token(self, username, password) -> dict:
        rsp = self.client.post(reverse('get-token'), {'username': username, 'password': password})
        data = self._get_data(rsp)
        return data

    def setUp(self) -> None:
        user = User.objects.create_user(**self.user_data)
        admin = User.objects.create_superuser(**self.admin_data)

        project = models.Project.objects.create(title='first project', description='text...', main_user=admin)
        models.Task.objects.create(
            title='first task',
            start_date=datetime(2024, 2, 5),
            end_date=datetime(2024, 3, 5),
            priority=models.Task.LOW_PRIORITY,
            status=models.Task.STATUS_PLANNED,
            user=admin,
            project=project
        )

        self.user = user
        self.admin = admin

    def test_delete_task_by_admin(self):
        token = self._get_token(self.admin_data['username'], self.admin_data['password'])
        self.client.delete('http://localhost:8000/api/tasks/1/', headers=self._headers(token['access']))
        self.assertEqual(len(models.Task.objects.all()), 0)

    def test_delete_task_by_user(self):
        token = self._get_token(self.user_data['username'], self.user_data['password'])
        self.client.delete('http://localhost:8000/api/tasks/1/', headers=self._headers(token['access']))
        self.assertEqual(len(models.Task.objects.all()), 1)
