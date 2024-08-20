from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from sparklabapi.models.user import User
from sparklabapi.models.idea import Idea
from sparklabapi.models.collection import Collection

class CollectionTests(APITestCase):
  def setUp(self):
        self.user = User.objects.create(username='testuser', uid='12345')
        
        self.idea1 = Idea.objects.create(
            title='Idea 1', 
            description='Description for idea 1', 
            saved=False, 
            user=self.user
        )
        self.idea2 = Idea.objects.create(
            title='Idea 2', 
            description='Description for idea 2', 
            saved=True, 
            user=self.user
        )

        self.collection = Collection.objects.create(
            user=self.user,
            name='My Collection',
            cover='http://example.com/cover.jpg'
        )
        self.collection.ideas.set([self.idea1, self.idea2])
        
        self.url = reverse('collection-list')

  def test_create_collection(self):
        data = {
            'user': self.user.id,
            'name': 'My Collection',
            'cover': 'http://example.com/cover.jpg',
            'ideas': [self.idea1.id, self.idea2.id]
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'My Collection')
        self.assertEqual(response.data['cover'], 'http://example.com/cover.jpg')
        self.assertEqual(len(response.data['ideas']), 2)
        
        collection = Collection.objects.get(id=response.data['id'])
        self.assertEqual(collection.name, 'My Collection')
        self.assertEqual(collection.cover, 'http://example.com/cover.jpg')
        self.assertEqual(list(collection.ideas.values_list('id', flat=True)), [self.idea1.id, self.idea2.id])

  def test_read_collection(self):
    url = reverse('collection-detail', kwargs={'pk':self.collection.id})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], self.collection.name)
    self.assertEqual(response.data['cover'], self.collection.cover)
    self.assertEqual(len(response.data['ideas']), self.collection.ideas.count())

  def test_update_collection(self):
      url = reverse('collection-detail', kwargs={'pk': self.collection.id})
      updated_data = {
          'user': self.user.id,
          'name': 'Updated Collection Name',
          'cover': 'http://example.com/updated_cover.jpg',
          'ideas': [self.idea2.id]  
      }
      response = self.client.put(url, updated_data, format='json')
            
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.collection.refresh_from_db()
      self.assertEqual(self.collection.name, 'Updated Collection Name')
      self.assertEqual(self.collection.cover, 'http://example.com/updated_cover.jpg')
      self.assertEqual(list(self.collection.ideas.values_list('id', flat=True)), [self.idea2.id])

  def test_delete_collection(self):
        url = reverse('user-detail', kwargs={'pk': self.collection.id})  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
