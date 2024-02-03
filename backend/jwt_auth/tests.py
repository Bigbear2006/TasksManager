import json
import time

from django.test import TestCase
from django.urls import reverse

from . models import User


class JWTAuthTestCase(TestCase):
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

    def setUp(self) -> None:
        User.objects.create_superuser(**self.admin_data)

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

    def test_get_admin_token_and_register_other_admin(self):
        rsp = self.client.post(reverse('get-token'), self.admin_data)
        data = self._get_data(rsp)

        rsp = self.client.post(
            reverse('register-admin'),
            self.admin2_data,
            headers=self._headers(data["access"])
        )
        data = self._get_data(rsp)
        return self.assertEqual(data['is_superuser'], True)

    def test_register_user_and_check_access_token_lifetime(self):
        rsp = self.client.post(reverse('register-user'), self.user_data)
        data = self._get_data(rsp)

        data = self._get_token(data['username'], self.user_data['password'])
        rsp1 = self.client.post(reverse('verify-token'), {'token': data['access']})

        time.sleep(5)

        rsp2 = self.client.post(reverse('verify-token'), {'token': data['access']})
        return self.assertEqual(rsp1.status_code, 200) and self.assertEqual(rsp2.status_code, 401)

    def test_get_user_info(self):
        rsp = self.client.post(reverse('register-user'), self.user_data)
        data = self._get_data(rsp)
        token = self._get_token(data['username'], self.user_data['password'])

        rsp = self.client.post(reverse('user-info'), headers=self._headers(token['access']))
        self.assertEqual(self._get_data(rsp)['username'], self.user_data['username'])
