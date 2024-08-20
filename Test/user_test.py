from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sparklabapi.models import User

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", uid="12345")

    def test_create_user(self):
        url = reverse('user-list')  
        data = {
            "username": "testuser",
            "uid": "12345"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        user_id = response.data['id']
        user = User.objects.get(id=user_id)

        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['uid'], '12345')

    def test_read_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['uid'], self.user.uid)

    def test_partial_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        partial_data = {
            'username': 'Partially Updated User Name',
        }
        response = self.client.patch(url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'Partially Updated User Name')
        self.assertEqual(self.user.uid, '12345') 

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        data = {
            "username": "updateduser",
            "uid": "12345"
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.uid, '12345')
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['uid'], '12345')

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
