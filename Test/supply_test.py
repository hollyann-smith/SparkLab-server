from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sparklabapi.models import Supply

class SupplyTests(APITestCase):
  def setUp(self):
    self.supply = Supply.objects.create(name="testsupply2")
    
  def test_create_supply(self):
      url = reverse('supply-list')
      data = {
          "name": "testsupply"
      }
      
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Supply.objects.count(), 2)
      
      supply_id = response.data['id']
      supply = Supply.objects.get(id=supply_id)
      
      self.assertEqual(supply.name, 'testsupply')
      self.assertEqual(response.data['name'], 'testsupply')

  def test_read_supply(self):
    url = reverse('supply-detail', kwargs={'pk': self.supply.id})
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['id'], self.supply.id)

  def test_delete_supply(self):
    url = reverse('supply-detail', kwargs={'pk': self.supply.id})
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Supply.objects.count(), 0)
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
