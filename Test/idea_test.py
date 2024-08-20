from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sparklabapi.models import User, Idea, Supply

class IdeaTests(APITestCase):

  def setUp(self):
        self.user = User.objects.create(username="testuser", uid="12345")
        self.supply1 = Supply.objects.create(name="glue")
        self.supply2 = Supply.objects.create(name="glitter")
        self.idea = Idea.objects.create(
            user = self.user,  
            title = "Glitter Slime",
            description = "A fun activity to make glittery slime.",
            saved = False,
            img = "http://example.com/slime.jpg",
        )
        self.idea.supplies.set([self.supply1.id, self.supply2.id])
        
        self.url = reverse('idea-list')

  def test_create_idea(self):
    
        url = reverse('idea-list')  
        data = {
            "user": self.user.id,  
            "title": "Glitter Slime",
            "description": "A fun activity to make glittery slime.",
            "saved": False,
            "img": "http://example.com/slime.jpg",
            "supplies": [self.supply1.id, self.supply2.id] 
        }


        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Glitter Slime')
        self.assertEqual(response.data['description'], 'A fun activity to make glittery slime.')
        self.assertEqual(response.data['img'], "http://example.com/slime.jpg")
        self.assertEqual(len(response.data['supplies']), 2)

        idea = Idea.objects.get(id=response.data['id'])
        self.assertEqual(idea.title, 'Glitter Slime')
        self.assertEqual(idea.description, 'A fun activity to make glittery slime.')
        self.assertEqual(idea.saved, False)
        self.assertEqual(idea.img, "http://example.com/slime.jpg")
        self.assertEqual(list(idea.supplies.values_list('id', flat=True)), [self.supply1.id, self.supply2.id])

  def test_read_idea(self):
    url = reverse('idea-detail', kwargs={'pk':self.idea.id})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(self.idea.title, 'Glitter Slime')
    self.assertEqual(self.idea.description, 'A fun activity to make glittery slime.')
    self.assertEqual(self.idea.saved, False)
    self.assertEqual(self.idea.img, "http://example.com/slime.jpg")
    self.assertEqual(len(response.data['supplies']), self.idea.supplies.count())

  def test_update_idea(self):
      url = reverse('idea-detail', kwargs={'pk': self.idea.id})
      updated_data = {
            "user": self.user.id,  
            "title": "UPDATED Glitter Slime",
            "description": "A fun activity to make glittery UPDATED slime.",
            "saved": False,
            "img": "http://example.com/slime.jpg",
            "supplies": [self.supply2.id] 
      }
      response = self.client.put(url, updated_data, format='json')
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.idea.refresh_from_db()
      
      self.assertEqual(self.idea.title, 'UPDATED Glitter Slime')
      self.assertEqual(self.idea.description, 'A fun activity to make glittery UPDATED slime.')
      self.assertEqual(self.idea.saved, False)
      self.assertEqual(self.idea.img, "http://example.com/slime.jpg")
      self.assertEqual(list(self.idea.supplies.values_list('id', flat=True)), [self.supply2.id])

  def test_delete_idea(self):
        url = reverse('idea-detail', kwargs={'pk': self.idea.id})  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Idea.objects.count(), 0) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
